"""
Created on 2014-9-2

@author: ilcwd
"""
from hodao.models import Base, engine


def main():
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    main()