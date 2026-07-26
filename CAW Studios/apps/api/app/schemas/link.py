from datetime import datetime
class LinkCreate(BaseModel):
    long_url: HttpUrl
    @field_validator('long_url')
    @classmethod
    def validate_url_scheme_and_host(cls, v):
        if v.scheme not in ('http', 'https'):
        
        # Prevent recursive shortening
        if v.host in ('localhost', '127.0.0.1', 'cawstudios.com'):
            raise ValueError('Cannot shorten links pointing to this domain')
        return v

class LinkResponse(BaseModel):
    id: int
    code: str
    long_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True
