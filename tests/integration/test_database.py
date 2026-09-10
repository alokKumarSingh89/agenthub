import uuid

import pytest
from sqlalchemy import select

from packages.database import Agent, AgentStatus, Database, Organization


@pytest.mark.asyncio
async def test_create_organization_and_agent() -> None:
    database = Database(
        "postgresql+asyncpg://agenthub:agenthub@localhost:5432/agenthub",
    )

    try:
        async with database.session_factory() as session:
            organization = Organization(
                name="Interview Demo Organization",
                slug=f"interview-demo-{uuid.uuid4().hex[:8]}",
            )

            session.add(organization)

            await session.flush()

            agent = Agent(
                organization_id=organization.id,
                name="Support Agent",
                description="Customer support AI agent",
                status=AgentStatus.DRAFT,
            )

            session.add(agent)

            await session.commit()

            result = await session.execute(
                select(Agent).where(
                    Agent.id == agent.id,
                ),
            )

            saved_agent = result.scalar_one()

            assert saved_agent.organization_id == organization.id
            assert saved_agent.name == "Support Agent"
            assert saved_agent.status == AgentStatus.DRAFT

    finally:
        await database.dispose()
