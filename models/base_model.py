#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import os

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models
    
    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update
    
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """__init__ method for BaseModel class
        Args:
            args (tuple): arguments
            kwargs (dict): key word arguments
        """
        if kwargs:
            for name, value in kwargs.items():
                if name != '__class__':
                    if name == 'created_at' or name == 'updated_at':
                        value = datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, name, value)
            if 'id' not in kwargs:
                setattr(self, 'id', str(uuid.uuid4()))
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
            models.storage.new(self)
    
    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)
    
    def __repr__(self):
        '''
            Return string representation of BaseModel class
        '''
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in my_dict.keys():
            del(my_dict["_sa_instance_state"])
        return my_dict
    
    def delete(self):
        """
        Deletes the current instance from the storage
        """
        models.storage.delete(self)
