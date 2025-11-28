class LVLs:
    '''
    класс лвлов
    '''
    def __init__(self, met, str):
        '''
        инициализация класса
        '''
        self.met = met
        self.str = str

    def lvl_1(self):
        if self.met == 'upper':
            return (self.str).upper()
        elif self.met == 'lower':
            return (self.str).lower()
        elif self.met == 'capitalize':
            return (self.str).capitalize()
        pass

    def lvl_2(self, d1, d2):
        if self.met == 'find':
            return ((self.str).find(d1) + 1, (self.str).find(d1) + 1 + len(self.str))
        elif self.met == 'refind':
            return ((self.str).refind(d1) + 1, (self.str).refind(d1) + 1 + len(self.str))
        elif self.met == 'replace':
            return (self.str).replace(d1, d2)
        elif self.met == 'count':
            return (self.str).count(d1)
        pass

    def lvl_3(self, d1):
        if self.met == 'split':
            return ((self.str).split(d1))
        if self.met == 'join':
            return (d1.join(list(self.str)))


a = input('Выберете уровень:')
if a == 'lvl 1':
    c = input('Введите строку:')b = input('Выберите метод:')ans = LVLs(met=b, str=c)
    print(f'Ответ:{ans.lvl_1}')

if a == 'lvl 2':
    c = input('Введите строку:')
    b1 = input('Выберите что хотите:')
    if 'вхождение первого' in b:
        b = 'find'
        d1 = b[b.refind(' ')+1:]
        d2 = 0
        ans = LVLs(met=b, str=c)
        print(f'Ответ:{ans.lvl_2(d1, d2)}')
    if 'вхождение последнего' in b:
        b = 'refind'
        d1 = b[b.refind(' ')+1:]
        d2 = 0
        ans = LVLs(met=b, str=c)
        print(f'Ответ:{ans.lvl_2(d1, d2)}')
    if 'заменить' in b:
        b = 'replace'
        d1 = b[b.find(' ')+1:b[b.find(' ')+1:].find(' ')]
        d2 = b[b.refind(' ')+1:]
        ans = LVLs(met=b, str=c)
        print(f'Ответ:{ans.lvl_2(d1, d2)}')
    if 'посчетать все буквы' in b:
        b = 'count'
        d1 = b1[-1]
        d2 = 0
        ans = LVLs(met=b, str=c)
        print(f'Ответ:{ans.lvl_2(d1, d2)}')

if a == 'lvl 3':
    c = input('Введите строку:')
    b = input('Выберите метод:')
    d1 = input('Выберите символ:')
    ans = LVLs(met=b, str=c)
    print(f'Ответ:{ans.lvl_3(d1)}')

