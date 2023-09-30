from dataclasses import dataclass, field


@dataclass
class _RequestData:
    state: int  = None
    slot: int = None
    side: int = None

@dataclass
class _ResponseData:
    success: bool = True
    errorCode: str = None
    state: int = None

    def to_dict(self):
        return {
            "success": self.success,
            "errorCode": self.errorCode,
            "state": self.state
        }

@dataclass
class RpcRequest:
    command: int
    data: _RequestData

@dataclass
class RpcResponse: 
    command: int
    data: _ResponseData