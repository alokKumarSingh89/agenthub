from enum import StrEnum


class Permission(StrEnum):
    AGENT_CREATE = "agent:create"
    AGENT_READ = "agent:read"
    AGENT_UPDATE = "agent:update"
    AGENT_DELETE = "agent:delete"

    CONVERSATION_CREATE = "conversation:create"
    CONVERSATION_READ = "conversation:read"

    USER_MANAGE = "user:manage"
