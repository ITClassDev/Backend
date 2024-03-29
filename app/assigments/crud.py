from sqlmodel.ext.asyncio.session import AsyncSession
import sqlalchemy
from sqlalchemy import select, update, or_
from fastapi import HTTPException
from fastapi import status as http_status
import uuid as uuid_pkg
from app.assigments.models import Task, Contest, Submit
from app.users.models import User
from app.assigments.schemas import TaskCreate, TaskLeaderBoard, ContestCreate, ContestSubmitGithub, SubmitSourceCode, ContestRead, ContestStatisticsSolved
from typing import List, Tuple
from datetime import datetime
import os
from app import settings
from app.core.files import read_file

class TasksCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskCreate, author_id: uuid_pkg.UUID) -> Task:
        values = task.dict()
        values["authorId"] = author_id
        try:
            task = Task(**values)
            self.session.add(task)
            if task.dayChallenge:
                query_1 = update(Task).where(Task.uuid != task.uuid).values(dayChallenge=False) # Set other as not day challenge
                await self.session.execute(query_1)
            await self.session.commit()
            await self.session.refresh(task)
            return task
        except sqlalchemy.exc.IntegrityError as e:  # type: ignore
            err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
            raise HTTPException(
                http_status.HTTP_400_BAD_REQUEST, detail=err_msg)
        
    def only_example_tests(self, task: Task) -> Task:
        task_new = task.dict()
        task_new["tests"] = list(filter(lambda test: 'demo' in test and test['demo'], task.tests))
        return Task.parse_obj(task_new)
    
    async def update(self, uuid: uuid_pkg.UUID, task: Task) -> Task:
        new_data = task.dict()
        query = update(Task).where(Task.uuid == uuid).values(**new_data)
        await self.session.execute(query)
        await self.session.commit()
        return task
        
    async def get(self, task_uuid: uuid_pkg.UUID, only_demo: bool = True) -> Task | None:
        query = select(Task).where(Task.uuid == task_uuid)
        results = await self.session.execute(query)
        task = results.scalar_one_or_none()
        if not task:
            raise HTTPException(
                http_status.HTTP_404_NOT_FOUND, detail="Task with such uuid not found")
        if only_demo: return self.only_example_tests(task)
        return task
        
        
    async def get_day_challenge(self, only_example_tests: bool = True) -> Task | None:
        query = select(Task).where(Task.dayChallenge == True)
        results = await self.session.execute(query)
        task = results.scalar_one_or_none()
        if not task:
            raise HTTPException(
                http_status.HTTP_404_NOT_FOUND, detail="No day challenge for now")
        if only_example_tests: return self.only_example_tests(task)
        return task
        
    async def get_all(self) -> List[Task]:
        results = await self.session.execute(select(Task).order_by(Task.created_at.desc()))
        return [tuple(row)[0] for row in results]
    
    async def search(self, query: str) -> List[Task]:
        results = await self.session.execute(select(Task.uuid, Task.title).filter(Task.title.like(f'%{query}%')))
        return results.fetchall()
    
    async def set_challenge(self, uuid: uuid_pkg.UUID) -> Task:
        query_0 = update(Task).where(Task.uuid == uuid).values(dayChallenge=True) # Set task as day challenge
        query_1 = update(Task).where(Task.uuid != uuid).values(dayChallenge=False) # Set other as not day challenge
        await self.session.execute(query_0)
        await self.session.execute(query_1)
        await self.session.commit()
        day_challenge = select(Task).where(Task.dayChallenge == True)
        day_challenge = await self.session.execute(day_challenge)
        return day_challenge.scalar_one_or_none()
    
    async def task_leaderboard(self, task_uuid: uuid_pkg.UUID, limit: int = 10) -> List[TaskLeaderBoard]:
        query = select(Submit.userId, Submit.uuid.label("submitId"), Submit.created_at, User.firstName, User.lastName, User.avatarPath, User.nickName).where(Submit.taskId == task_uuid, Submit.solved == True, Submit.userId == User.uuid).order_by(Submit.created_at.asc()).limit(limit)
        results = await self.session.execute(query)
        uids = []
        def filter_unique(entry: list):
            if entry[0] not in uids:
                uids.append(entry[0])
                return True
            return False
        
        return list(filter(filter_unique, results.fetchall()))


class ContestsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, contest: ContestCreate, user_uuid: uuid_pkg.UUID) -> Contest:
        values = contest.dict()
        values["authorId"] = user_uuid
        try:
            contest = Contest(**values)
            self.session.add(contest)
            await self.session.commit()
            await self.session.refresh(contest)
            return contest
        except sqlalchemy.exc.IntegrityError as e:  # type: ignore
            err_msg = str(e.orig).split(':')[-1].replace('\n', '').strip()
            raise HTTPException(
                http_status.HTTP_400_BAD_REQUEST, detail=err_msg)
    
    async def get_all(self) -> List[Contest]:
        results = await self.session.execute(select(Contest).order_by(Contest.updated_at.desc()))
        return [tuple(row)[0] for row in results]
    
    async def get(self, uuid: uuid_pkg.UUID) -> Contest:
        results_ = await self.session.execute(select(Contest).where(Contest.uuid == uuid))
        contest = results_.scalar_one_or_none()
        contest_work = contest.dict().copy()
        contest_tasks = contest_work["tasks"]
        contest_work["tasks"] = []
        if contest:
            for task_uuid in contest_tasks:
                query = select(Task.title).where(Task.uuid == task_uuid)
                results = await self.session.execute(query)
                contest_work["tasks"].append({"uuid": task_uuid, "title": results.scalar_one_or_none()})
            return contest_work
        raise HTTPException(http_status.HTTP_404_NOT_FOUND, detail="No contest with such UUID")
    
    async def extended_get(self, uuid: uuid_pkg.UUID) -> Contest:
        '''
        Only for local usage inside crud and checker pipeline
        '''
        results_ = await self.session.execute(select(Contest).where(Contest.uuid == uuid))
        contest = results_.scalar_one_or_none()
        contest_work = contest.dict().copy()
        contest_tasks = contest_work["tasks"]
        contest_work["tasks"] = []
        if contest:
            for task_uuid in contest_tasks:
                query = select(Task.functionName, Task.tests, Task.testsTypes, Task.timeLimit, Task.memoryLimit).where(Task.uuid == task_uuid)
                results = await self.session.execute(query)
                results = results.fetchall()[0]
                # print(results)
                if results:
                    contest_work["tasks"].append({"uuid": task_uuid, "function_name": results[0], "tests": results[1], "types": results[2], "time": results[3], "memory": results[4]})
            return contest_work
        raise HTTPException(http_status.HTTP_404_NOT_FOUND, detail="No contest with such UUID")
    
    async def get_active_for_user(self, user_uuid: uuid_pkg.UUID, user_group: uuid_pkg.UUID, user_class: int) -> List[ContestRead]:
        query = select(Contest).where(Contest.forLearningClass == user_class, Contest.forGroups.contains([user_group]), Contest.deadline >= datetime.utcnow())
        results = await self.session.execute(query)
        results = [ContestRead(**tuple(row)[0].dict()) for row in results]
        for index, contest in enumerate(results):
            tmp = await self.session.execute(select(Submit.taskId).where(Submit.referedContest == contest.uuid, Submit.userId == user_uuid, Submit.solved == True))
            results[index].solvedPercentage = len([tuple(row)[0] for row in tmp.fetchall()]) / len(contest.tasks) * 100
        return results
    
    async def get_solved_tasks(self, contest_uuid: uuid_pkg.UUID, user_uuid: uuid_pkg.UUID) -> Tuple[List[uuid_pkg.UUID], List[uuid_pkg.UUID]]: 
        results = await self.session.execute(select(Submit.taskId).where(Submit.referedContest == contest_uuid, Submit.userId == user_uuid, Submit.solved == True))
        solved = [tuple(row)[0] for row in results.fetchall()]
        results = await self.session.execute(select(Submit.taskId).where(Submit.referedContest == contest_uuid, Submit.userId == user_uuid, Submit.solved == False, or_(Submit.status == 2, Submit.status == 3))) # not solved and rejected or checked
        failed = [tuple(row)[0] for row in results.fetchall()]
        return solved, failed
        
    async def statistics(self, uuid: uuid_pkg.UUID) -> Tuple[int, List[ContestStatisticsSolved]]:
        contest = await self.session.execute(select(Contest).where(Contest.uuid == uuid))
        contest = contest.scalar_one_or_none()
        statistics = []
        if contest:
            affected_users = await self.session.execute(select(User.uuid, User.nickName, User.avatarPath, User.firstName, User.lastName).where(User.learningClass == contest.forLearningClass, User.groupId.in_(contest.forGroups)))
            affected_users = affected_users.fetchall()
            for user in affected_users:
                all_submits = await self.session.execute(select(Submit.uuid, Submit.solved).where(Submit.userId == user.uuid, Submit.referedContest == contest.uuid).order_by(Submit.created_at))
                all_submits = all_submits.fetchall()
                pointer = 0
                solved_count = 0
                mark = 2
                while pointer < len(all_submits):
                    if all_submits[pointer].solved:
                        solved_count += 1
                    else:
                        break
                    pointer += 1
                if solved_count >= contest.mark5: mark = 5
                elif solved_count >= contest.mark4: mark = 4
                elif solved_count >= contest.mark3: mark = 3
                else: mark = 2
                statistics.append(ContestStatisticsSolved(userId=user.uuid, nickName=user.nickName, avatarPath=user.avatarPath, firstName=user.firstName, lastName=user.lastName, solvedCount=solved_count, mark=mark))
            return len(contest.tasks), [contest.mark5, contest.mark4, contest.mark3], statistics
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="No such contest")

class SubmitsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.tasks_crud = TasksCRUD(self.session)

    async def get_users_for_tasks(self, task_uuid: uuid_pkg.UUID, user_uuid: uuid_pkg.UUID):
        query = select(Submit).where(Submit.userId == user_uuid, Submit.taskId == task_uuid)
        results = await self.session.execute(query)
        return results.fetchall()
    
    async def get_users_refered_for_contest_task(self, task_uuid: uuid_pkg.UUID, contest_uuid: uuid_pkg.UUID, user_uuid: uuid_pkg.UUID):
        query = select(Submit).where(Submit.userId == user_uuid, Submit.taskId == task_uuid, Submit.referedContest == contest_uuid).order_by(Submit.created_at.desc())
        results = await self.session.execute(query)
        return [tuple(row)[0] for row in results.fetchall()]
    
    async def submit(self, source: str, user_uuid: uuid_pkg.UUID, task_uuid: uuid_pkg.UUID = None, task_object: Task = None, referedContest: uuid_pkg.UUID | None = None) -> Submit:
        '''
        Task uuid based used in contest's endpoints
        Direct task object used in day challenge, to prevent day challenge reselect
        '''
        # Resolve task obj
        # Statuses: 0 - Pending; 1 - Checking; 2 - Checked; 3 - rejected
        task = task_object
        if not task: task = await self.tasks_crud.get(task_uuid)
        task_uuid = task.uuid
        submit = Submit(status=1, taskId=task_uuid, source=source, solved=False, userId=user_uuid, referedContest=referedContest)
        self.session.add(submit)
        await self.session.commit()
        await self.session.refresh(submit)
        return submit

    async def get(self, uuid: uuid_pkg.UUID, user_id: uuid_pkg.UUID) -> Submit:
        query = select(Submit).where(Submit.uuid == uuid and Submit.userId == user_id)
        results = await self.session.execute(query)
        result_object = results.scalar_one_or_none()
        if result_object.userId == user_id:
            result_object = result_object.dict()
            if not result_object["referedContest"]:
                result_object["source"] = await read_file(result_object["source"], os.path.join(settings.user_storage, "tasks_source_codes"))
            else:
                result_object["source"] = result_object["source"]
            return result_object
        raise HTTPException(
            http_status.HTTP_404_NOT_FOUND, detail="No such submit or it is not your submit"
        )
    
    async def get_source_code(self, uuid: uuid_pkg.UUID) -> SubmitSourceCode:
        query = select(Submit).where(Submit.uuid == uuid)
        results = await self.session.execute(query)
        results = results.scalar_one_or_none()
        
        if results:
            source = await read_file(results.source, os.path.join(settings.user_storage, "tasks_source_codes"))
            return SubmitSourceCode(source=source, language={"cpp": "c++", "py": "python"}[results.source.split(".")[-1]])
        raise HTTPException(
            http_status.HTTP_404_NOT_FOUND, detail="No such submit"
        )

    async def submit_day_challenge(self, source: str, user_uuid: uuid_pkg.UUID) -> Tuple[Submit, Task]:
        day_challenge = await self.tasks_crud.get_day_challenge(only_example_tests=False) # Get all tests
        if day_challenge:
            return await self.submit(source, user_uuid, task_object=day_challenge), day_challenge
            
        raise HTTPException(
            http_status.HTTP_400_BAD_REQUEST, detail="No day challenge for now")
    
    def checker_callback(self, data: dict, loop: object) -> None:
        '''
        Sync function!
        '''
        solved, tests_results_log, submit_id = data["status"], data["tests"], uuid_pkg.UUID(data["submit_id"])
        print(solved, tests_results_log, submit_id)
        query = update(Submit).where(Submit.uuid == submit_id).values(status=2, solved=solved, testsResults=tests_results_log)
        async def commit_async():
            await self.session.execute(query)
            await self.session.commit()
        loop.create_task(commit_async())

    def checker_save_results(self, data: dict, loop: object) -> None:
        '''
        Sync function!
        '''
        async def commit_async(queries):
            for query in queries:
                await self.session.execute(query)
            await self.session.commit()

        pending = []
        for submit in data:
            solved, tests_results_log, submit_id = submit["solved"], submit["tests_results"], uuid_pkg.UUID(submit["submit_id"])
            query = update(Submit).where(Submit.uuid == submit_id).values(status=2, solved=solved, testsResults=tests_results_log)
            pending.append(query)
        loop.create_task(commit_async(pending))

    async def submit_contest(self, contest_submit: ContestSubmitGithub, user_uuid: uuid_pkg.UUID) -> List[dict]:
        contests_crud = ContestsCRUD(self.session)
        contest = await contests_crud.extended_get(contest_submit.contest)
        
        submits_payloads = []
        for task in contest["tasks"].copy():
            tmp_submit = await self.submit(contest_submit.githubLink, user_uuid, task["uuid"], referedContest=contest_submit.contest)
            submits_payloads.append({
                "name": task["function_name"],
                "tests": task["tests"],
                "submit_id": str(tmp_submit.uuid),
                "types": {
                    "in": task["types"]["input"],
                    "out": task["types"]["output"][0]
                },
                "env": {"mem": task["memory"], "proc": 2, "time": task["time"]}
            })


        await self.session.commit()
        return submits_payloads
    
    async def day_challenge_user_submits(self, user_uuid: uuid_pkg.UUID) -> List[Submit]:
        day_challenge = await self.tasks_crud.get_day_challenge()
        if day_challenge:
            query = select(Submit).where(Submit.userId == user_uuid, Submit.taskId == day_challenge.uuid, Submit.referedContest.is_(None)).order_by(Submit.created_at.desc())
            results = await self.session.execute(query)
            return [tuple(row)[0] for row in results.fetchall()]
            
        raise HTTPException(
            http_status.HTTP_400_BAD_REQUEST, detail="No day challenge for now")
    

    async def reject(self, submit_uuid: uuid_pkg.UUID) -> None:
        print(submit_uuid)
        query = update(Submit).where(Submit.uuid == submit_uuid).values(solved=False, status=3) # Set rejected (3) status to submit
        await self.session.execute(query)
        await self.session.commit()
    