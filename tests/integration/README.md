# tests/integration/

End-to-end wiring tests for `main()` functions of stages using mocks for heavy dependencies (network, OpenAI).

Uses `PipelineStages` injection in `test_pipeline_flow` to avoid mocks on orchestration.

See [`../TESTING.md`](../TESTING.md) and parent [`../README.md`](../README.md).
