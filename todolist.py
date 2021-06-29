from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit")
while True:
    dec = input()
    if dec == '':
        break
    elif dec == '0':
        print('Bye')
        break
    elif dec == '1':
        rows = session.query(Table).all()
        print('Today', datetime.today().day, datetime.today().strftime('%b'))
        today_tasks = []
        for elem in rows:
            if elem.deadline == datetime.date(datetime.today()):
                today_tasks.append(elem.task)
        if not today_tasks:
            print('Nothing to do!')
        else:
            for i in range(len(today_tasks)):
                print(f'{i + 1}. {today_tasks[i]}')
    elif dec == '2':
        rows = session.query(Table).all()
        week = [str(datetime.date(datetime.today() + timedelta(days=i))) for i in range(7)]
        week_tasks = {str((datetime.date(datetime.today() + timedelta(days=i)))): [] for i in range(7)}
        for elem in rows:
            if str(elem.deadline) in week:
                week_tasks[str(elem.deadline)].append(elem.task)
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for key, value in week_tasks.items():
            key = datetime.strptime(key, '%Y-%m-%d')
            print()
            print(weekdays[key.weekday()], key.day, key.strftime('%b') + ':')
            if not value:
                print('Nothing to do!')
            else:
                for i in range(len(value)):
                    print(f'{i + 1}. {value[i]}')
    elif dec == '3':
        print('All tasks:')
        rows = session.query(Table).order_by(Table.deadline).all()
        for i in range(len(rows)):
            print(f'{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime("%b")}')
    elif dec == '4':
        print('Enter task')
        task = input()
        print('Enter deadline')
        deadline = input()
        new_row = Table(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
        session.add(new_row)
        session.commit()
        print('The task has been added!')
