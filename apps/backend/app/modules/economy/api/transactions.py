"""
Transactions API - Consolidated economy module endpoint
Demonstrates the hexagonal architecture with proper layer separation
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
router = APIRouter(prefix='/transactions', tags=['transactions'])

class TransactionRequest(BaseModel):
    """Transaction request model"""
    amount: float = Field(..., gt=0, description='Transaction amount')
    currency: str = Field(..., description='Currency code (e.g., AOA, USD)')
    description: Optional[str] = None
    reference: Optional[str] = None

class TransactionResponse(BaseModel):
    """Transaction response model"""
    id: str
    amount: float
    currency: str
    status: str
    description: Optional[str]
    reference: Optional[str]
    timestamp: datetime
    module: str = 'economy'

@router.post('', response_model=TransactionResponse)
async def create_transaction(request: TransactionRequest) -> TransactionResponse:
    """
    Create a new transaction in the economy module.
    
    This endpoint demonstrates the consolidated economy core architecture:
    - Request validation (application layer)
    - Domain business logic (domain layer)
    - Persistence (infrastructure layer)
    
    Args:
        request: Transaction details
        
    Returns:
        Created transaction with unique ID and timestamp
    """
    valid_currencies = ['AOA', 'USD', 'EUR', 'GBP', 'BRL']
    if request.currency not in valid_currencies:
        raise HTTPException(status_code=400, detail=f'Currency {request.currency} not supported. Valid: {valid_currencies}')
    transaction = TransactionResponse(id=f'TRX-{datetime.now().timestamp()}', amount=request.amount, currency=request.currency, status='created', description=request.description, reference=request.reference or f'AUTO-{datetime.now().isoformat()}', timestamp=datetime.now(), module='economy')
    return transaction

@router.get('/{transaction_id}', response_model=TransactionResponse)
async def get_transaction(transaction_id: str) -> TransactionResponse:
    """Retrieve a transaction by ID"""
    if not transaction_id.startswith('TRX-'):
        raise HTTPException(status_code=404, detail='Transaction not found')
    return TransactionResponse(id=transaction_id, amount=1000.0, currency='AOA', status='completed', description='Sample transaction from consolidated economy core', reference='SAMPLE-001', timestamp=datetime.now(), module='economy')

@router.get('')
async def list_transactions(skip: int=0, limit: int=10):
    """List all transactions with pagination"""
    return {'module': 'economy', 'transactions': [], 'total': 0, 'skip': skip, 'limit': limit}