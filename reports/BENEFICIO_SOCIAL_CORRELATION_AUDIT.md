# Beneficio Social Correlation Audit

## success
- PedidoBeneficioEvent: correlation_id=7ce4f326-d963-4f4a-9c7c-88741e09d2c0, causation_id=None
- VerificacaoNifConcluidaEvent: correlation_id=7ce4f326-d963-4f4a-9c7c-88741e09d2c0, causation_id=7bc2a6b7-2a92-42a0-a284-c7d9763f2531
- VerificacaoSSConcluidaEvent: correlation_id=7ce4f326-d963-4f4a-9c7c-88741e09d2c0, causation_id=cf1013d2-8fba-47cc-96a1-4a20ff9123a4
- BeneficioAprovadoEvent: correlation_id=7ce4f326-d963-4f4a-9c7c-88741e09d2c0, causation_id=992cc2e0-eaf2-4227-820f-375d3a885437

## reject
- PedidoBeneficioEvent: correlation_id=13eae692-3ecb-44d6-9084-be5268ee1d6e, causation_id=None
- VerificacaoNifConcluidaEvent: correlation_id=13eae692-3ecb-44d6-9084-be5268ee1d6e, causation_id=f5bb7e86-0c64-4a7d-81ea-ddd575442c3e
- VerificacaoSSConcluidaEvent: correlation_id=13eae692-3ecb-44d6-9084-be5268ee1d6e, causation_id=c8d7131e-e417-407f-ae5e-7542cf0c6955

## cancel
- PedidoBeneficioEvent: correlation_id=69bf04d1-380a-4287-91a0-57138d6bfd79, causation_id=None
- VerificacaoSSConcluidaEvent: correlation_id=69bf04d1-380a-4287-91a0-57138d6bfd79, causation_id=4cf95b26-13e8-4c60-8091-5249c84d2413

