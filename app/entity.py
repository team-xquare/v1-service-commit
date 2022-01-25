from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class Commit():
    github_id: str
    week_commit_count: int
    total_commit_count: int
    order_criteria: str # 정렬하는 기준을 선택한다 week | total 둘중에 하나 선택

    def __lt__(self, other):
        if self.order_criteria == 'week':
            return self.week_commit_count > other.week_commit_count
        if self.order_criteria == 'total':
            return self.total_commit_count > other.total_commit_count
        return self.week_commit_count > other.week_commit_count
            