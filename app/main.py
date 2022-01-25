from fastapi import FastAPI, HTTPException
from typing import List

from app.entity import Commit

import json
import aioredis

from dotenv import load_dotenv
load_dotenv()

redis = aioredis.from_url('redis://redis')
app = FastAPI()

@app.get("/v1/commits/rank/{github_id}", response_model=Commit)
async def read_my_commits_rank(github_id: str):
    commit = Commit(
                github_id=github_id,
                order_criteria=None,
                **json.loads(await redis.get(github_id))
            )

    return commit


@app.get("/v1/commits/rank", response_model=List[Commit])
async def read_commits_rank(sort: str='week'):
    github_ids = await redis.keys("*")
    response: List[Commit] = []

    if sort != 'week' and sort != 'total':
        return HTTPException(status_code=400, detail='sort는 week나 total만 가능합니다.')

    cache = await redis.get(f'sorted_{sort}_commits') # sorted_week_commits or sorted_total_commits
    if not cache:
        for github_id in github_ids:
            commit = Commit(
                github_id=github_id.decode(),
                order_criteria=sort,
                **json.loads(await redis.get(github_id))
            )
            response.append(commit)
        response.sort()
        await redis.set(f'sorted_{sort}_commits', json.dumps([r.__dict__ for r in response]))
    response = json.loads(await redis.get(f'sorted_{sort}_commits'))

    return response
