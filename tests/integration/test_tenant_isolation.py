import uuid

import pytest
from sqlalchemy import select

from packages.database import Agent, AgentStatus, Database, Organization

DATABASE_URL = "postgresql+asyncpg://agenthub:agenthub@localhost:5432/agenthub"


@pytest.mark.asyncio
async def test_agent_query_can_be_scoped_to_organization() -> None:
    database = Database(DATABASE_URL)

    try:
        async with database.session_factory() as session:
            organization_a = Organization(
                name="Organization A",
                slug=f"organization-a-{uuid.uuid4().hex[:8]}",
            )

            organization_b = Organization(
                name="Organization B",
                slug=f"organization-b-{uuid.uuid4().hex[:8]}",
            )

            session.add_all(
                [
                    organization_a,
                    organization_b,
                ],
            )

            await session.flush()

            agent_a = Agent(
                organization_id=organization_a.id,
                name="Agent A",
                status=AgentStatus.ACTIVE,
            )

            agent_b = Agent(
                organization_id=organization_b.id,
                name="Agent B",
                status=AgentStatus.ACTIVE,
            )

            session.add_all(
                [
                    agent_a,
                    agent_b,
                ],
            )

            await session.commit()

            result = await session.execute(
                select(Agent).where(
                    Agent.organization_id == organization_a.id,
                ),
            )

            agents = result.scalars().all()

            assert len(agents) == 1
            assert agents[0].id == agent_a.id
            assert agents[0].organization_id == organization_a.id

    finally:
        await database.dispose()
