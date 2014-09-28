"""
Created on 2014-9-2

@author: ilcwd
"""

# init config first!
import wsgiapp

from hodao.models import Base, engine


def main():
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

    # for i in engine.execute('SELECT * FROM "contact"'):
    #     print i


if __name__ == '__main__':
    main()