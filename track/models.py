from django.db import models

# Create your models here.
# purpose Tracking  engineering issue 
from abc import ABC, abstractmethod

class BaseEntity(ABC): 
    @abstractmethod
    def validate(self): 
        pass

    def to_dict(self): 
        return {
            key: value
            for key, value in self.__dict__.items() :
            pass
        }

class Reporter(BaseEntity): 
    def __init__(self, id, name, email, team): 
        self.id = id
        self.name  = name
        self.email = email 
        self.team = team  

    def validate(self): 
        if not self.name: 
            raise ValueError("Name  cannot be empty")
        if "@" not in self.email: 
            raise ValueError("Invalid email")
            
    name = models.CharField(max_length=254)
    email = models.EmailField()
    team = models.CharField(choices=["backend", "frontend", "devops"])


class Issue(models.Model): 
    reporter_id = models.ForeignKey(Reporter)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(choices=["open", "in_progress", "ressolved", "closed"])
    priority = models.CharField(choices=["low", "medium", "high", "critical"])
    crated_at = models.DateTimeField(auto_now=True)
    