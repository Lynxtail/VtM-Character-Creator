class Character:
    __name = ''
    __attributes = dict()
    __skills = dict()
    __clan = ''
    
    def __init__(self, name:str = '???', 
                 attributes:dict = {}, 
                 skills:dict = {}, 
                 clan:str = '???') -> None:
        self.__name = name
        self.__attributes = attributes
        self.__skills = skills
        self.__clan = clan
    
    def get_info(self):
        return f'Имя: {self.__name}/n\
                Атрибуты: {self.__attributes}/n\
                Навыки: {self.__skills}/n\
                Клан: {self.__clan}'
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if isinstance(name, str) and name:
            self.__name = name
        else: raise Exception
    
    @property
    def clan(self):
        return self.__clan
    
    @clan.setter
    def clan(self, clan):
        if isinstance(clan, str) and clan:
            self.__clan = clan
        else: raise Exception

    @property
    def attributes(self):
        return self.__attributes
    
    @attributes.setter
    def attributes(self, attributes):
        if isinstance(attributes, dict) and attributes:
            self.__attributes = attributes
        else: raise Exception
    
    @property
    def skills(self):
        return self.__skills
    
    @skills.setter
    def skills(self, skills):
        if isinstance(skills, dict) and skills:
            self.__skills = skills
        else: raise Exception