import json
import uuid

from random import random

from sqlalchemy import update
from sqlalchemy.orm import Session

from db.connection import engine
from db.goal.goal_table import GoalTable

from consumer.base_consumer import BaseConsumer

# from model.goal_model import GoalModel


def insertData(uid, phase, turn, file, predict, _max):
    with Session(engine) as session:
        session.add(
            GoalTable(
                uuid=uid,
                phase=phase,
                turn=turn,
                predict=str(predict),
                max=_max,
                file=file,
            )
        )
        session.commit()


def updateData(uid, real):
    with Session(engine) as session:
        session.execute(
            update(GoalTable).where(GoalTable.uuid == uid).values(real=real)
        )
        session.commit()


class GoalConsumer(BaseConsumer):
    def __init__(self, ENV):
        super().__init__(ENV)
        # self.model = GoalModel()

    def on_message(channel, method_frame, header_frame, body):
        data = json.loads(body.decode())

        if data["type"] == "request":
            uid = str(uuid.uuid4())
            turn = data["turn"]
            phase = data["phase"] if "phase" in data.keys() else str(uuid.uuid4())

            f = open(data["filename"], "rb")
            predict = [random() for _ in range(5)]
            _max = predict.index(max(predict))

            insertData(uid, phase, turn, f, predict, _max)

            channel.basic_publish(
                "",
                routing_key=header_frame.reply_to,
                body=json.dumps(
                    {"phase": phase, "uuid": uid, "angle": _max - 3, "ok": True}
                ),
            )

        if data["type"] == "result":
            uid = data["uuid"]
            result = data["result"]

            updateData(uid, result)

            channel.basic_publish(
                "",
                routing_key=header_frame.reply_to,
                body=json.dumps({"ok": True}),
            )
