from fastapi import FastAPI

import aioredis

app = FastAPI()
redis = aioredis.from_url('redis://redis')


@app.get("/v1/commits/rank/{github_id}")
async def read_my_commits_rank(github_id: str):
    commits_info = await redis.get(github_id)

    return commits_info


@app.get("/v1/commits/rank")
async def read_commits_rank():
    pass
