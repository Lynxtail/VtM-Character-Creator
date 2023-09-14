class Character:
    __name = ''
    # __attributes = dict().fromkeys((range(9)))
    __attributes = dict()
    __skills = dict()
    __clan = ''
    
    def __init__(self, name:str = '???', 
                 attributes:dict = {}, 
                 skills:dict = {}, 
                 clan:str = '???') -> None:
        self.__name = name
        if attributes:
            self.__attributes = attributes
        else:
            self.__attributes = {key : 0 for key in ('сила', 'харизма', 'интеллект', 
                  'ловкость', "манипулирование", "смекалка", 
                  "выносливость", "самообладание", "решительность")}
        if attributes:
            self.__skills = skills
        else:
            self.__skills = {key : 0 for key in ('сила', 'харизма', 'интеллект', 
                  'ловкость', "манипулирование", "смекалка", 
                  "выносливость", "самообладание", "решительность")}
        self.__clan = clan
    
    def get_info(self):
        ans = f'Имя: {self.__name}'
        ans += f'\nКлан: {self.__clan}'
        ans += f'\n\nАтрибуты:\n'
        if self.__attributes:
            for (key, value) in self.__attributes.items():
                ans += f'{key.capitalize():17}{value}\n'
        ans += '\n\nНавыки:\n'        
        if self.__skills:
            for (key, value) in self.__skills.items():
                ans += f'{key.capitalize():17}{value}\n'
        return ans
    
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