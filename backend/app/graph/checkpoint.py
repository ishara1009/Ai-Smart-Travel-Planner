from langgraph.checkpoint.memory import InMemorySaver

# Application records are durable in MongoDB. This checkpointer preserves in-process
# graph state between related operations; it can be replaced by a durable saver later.
checkpointer = InMemorySaver()
