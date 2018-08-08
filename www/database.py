from models import Match
from models import Result
from models import Team

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import json
import os

class Database(object):
    
    db_user = os.getenv("DB_USER") if os.getenv("DB_USER") != None else "example"
    db_pass = os.getenv("DB_PASS") if os.getenv("DB_PASS") != None else "example"
    db_host = os.getenv("DB_HOST") if os.getenv("DB_HOST") != None else "db"
    db_name = os.getenv("DB_NAME") if os.getenv("DB_NAME") != None else "tp2"
    db_port = os.getenv("DB_PORT") if os.getenv("DB_PORT") != None else "3306"
    # Base = declarative_base()


    def get_session(self):
        """Singleton of db connection

        Returns:
            [db connection] -- [Singleton of db connection]
        """
        
        connection = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (self.db_user,self.db_pass,self.db_host,self.db_port,self.db_name)
        engine = create_engine(connection,echo=True)
        connection = engine.connect()
        Session = sessionmaker(bind=engine)        
        session = Session()
        return session

    def init_match(self, dict_match):
        """Generate the match in the database
    
        Returns:
            [id of match] -- [generate the two results and the match]
        """
        session = self.get_session()
        m = Match(place=dict_match["place"])
        session.add(m)
        session.commit()
        r1 = Result(id_match=m.id,id_team=dict_match["team1"])
        r2 = Result(id_match=m.id,id_team=dict_match["team2"])
        session.add(r1)
        session.add(r2)
        session.commit()     
        return m.id
    
    def get_all_zone_teams(self, zone):
        """Return all teams from a specific zone
        
        Arguments:
            zone {[int]} -- [The zone. 1 is for WEST | 2 is for EAST]
        
        Returns:
            [array] -- [return a array with the id, name and logo of the teams ]
        """

        result = self.get_session().query(Team).filter_by(id_zone = zone)
        self.get_session().close()
        return [r.serialize() for r in result]
        
    def get_match(self, id_match):

        match = self.get_session().query(Match).filter_by(id=id_match)
        self.get_session().close()
        return match[0].serialize()

    def get_result_match(self, id_match):

        results = self.get_session().query(Result).filter_by(id_match=id_match)
        self.get_session().close()
        result_match = [{
            'id_team': results[0].id_team,
            'score': results[0].score
        },{
            'id_team': results[1].id_team,
            'score': results[1].score
        }]        
        return result_match

    def get_team(self, id_team):
        
        team = self.get_session().query(Team).filter_by(id=id_team)
        self.get_session().close()
        return team[0].serialize()
    