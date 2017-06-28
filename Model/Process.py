from Model.Task import *
from Util.Functions import *
class Process():
    def __init__(self, entrada):
        self.dependences = []
        self.executados = []
        self.opened = ''
        self.entrada = ''
        self.tasks = []
        self.domain = None
        self.entrada = entrada
        self.visited = False

    def carregar(self):
        # Independencia: simbolo: *
        # Dependencia: simbolo: <
        #   Strict Dependence(dependencia rigorosa): B so pode executar se A tiver sido, simbolo:
        #   Circumstancial Dependence: B pode executar se A tiver sido ou não executado nenhuma vez
        # Non-coexistence: sets {a} and {b} simbolo: # , conjunto a so pode executar se o b nao existir
        # Uniao: flow ex a, flow b, flow ex a and b

        # Paralelo: + (conjunto)
        # Or: o (conjunto)
        # Exclusive: x (conjunto)
        a = 0
        print('Entrada: ', end='')
        print(self.entrada)
        for str in self.entrada:
            self.tasks.append(task(str, a))
            self.tasks[a].treat()
            if self.tasks[a].legend == 'domain':
                self.domain = self.tasks[a]
            if self.tasks[a].legend == 'dependence':
                self.dependences.append(self.tasks[a])
            a += 1

        for i in [k for k in range(0, len(self.tasks)) if self.tasks[k].legend != 'domain']:  # if tasks[k].legend == 'paralell']:
            for u in [k for k in range(0, len(self.tasks)) if self.tasks[k].legend != 'domain']:  # if tasks[k].legend == 'or']:
                if self.tasks[i].id != self.tasks[u].id:
                    # print(tasks[i].cs, tasks[u].cs)
                    true = 0

                    groupset_x = self.tasks[i].cs
                    groupset_y = self.tasks[u].cs
                    for choiceset_x in groupset_x:
                        for choiceset_y in groupset_y:
                            # print(choiceset_x, ' ', choiceset_y)
                            intersection = Functions.intersect(choiceset_x, choiceset_y)
                            if len(intersection) > 0 and len(choiceset_y) == 1:
                                true += 1
                                if true == len(self.tasks[u].cs):
                                    # Repito o passo e verifico se tem alguma anormalidade...

                                    # print(','.join(tasks[u].cs), end='')
                                    # print(' -> ', end='')
                                    # p = ''.join(tasks[u].cs)
                                    self.tasks[i].relationships += [self.tasks[u].id]
                                    #self.tasks[u].relationships += [self.tasks[i].id]
                        if true == 1 and self.tasks[u].legend != 'dependence' and self.tasks[i].legend != 'dependence':
                            p = ';'.join(self.tasks[u].cs)
                            q = ';'.join(''.join(a) for a in self.tasks[i].cs)
                            string = ("Erro: %s nao pode estar contido em dois diferentes choicesets %s" % (p, q))
                            raise Exception(string)

        domain = [k for k in range(0, len(self.tasks)) if self.tasks[k].legend == 'domain'][0]
        list_with_no_virgulas = self.tasks[domain].cs[0].split(',')
        # gerando os recommendation points
        trocas = 0

        for i in [k for k in range(0, len(self.tasks)) if self.tasks[k].legend == 'domain']:
            for u in [k for k in range(0, len(self.tasks)) if self.tasks[k].legend == 'dependence']:
                if self.tasks[i].id != self.tasks[u].id:
                    dependention = self.tasks[u].cs[0]
                    list_with_no_virgulas = self.tasks[i].cs[0].split(',')
                    try:
                        list_with_no_virgulas.remove(dependention)
                        trocas += 1
                    except:
                        pass

        print('dominio: ', end='-> ')
        print(list_with_no_virgulas)
        print('conjunto de atividades-> ', end=' ')
        print(Functions.generate_possibilities(list_with_no_virgulas))

    def step_2(self):
        # Mostrando as ligações dos elementos primeiramente

        for task in reversed(self.tasks):
            print(str(task.taskstr), end=': ')
            for i in range(len(task.relationships)):
                task_rel = self.get_taskbyid(task.relationships[i])
                print(task_rel.taskstr, end=',')

            print('')
        # Teste

        tarefas = []
        for task in reversed(self.tasks):
            if task.legend != 'domain':
                tarefas += [task]

        tarefa = self.leitura_arvore(self.get_first_or())
        lista_combinacoes = {}
        print('\nGerando as combinações para o elemento: ')

        # As vezes a lista contém mais de um elemento separado por uma vírgula, dessa forma
        # É necessário fazer um split e percorrer elemento por elemento

        # Aqui eu remvo todos do dominio para deixar apenas os avulsos
        splitted = self.domain.cs[0].split(',')
        for i in tarefas:
            for k in i.cs:
                for ele in k.split(','):
                    try:
                        splitted.remove(ele)
                    except Exception as e:
                        pass

        # Apos remover todos que estão em choice sets, eu então crio eles separadamente
        lst = {}
        id_lst = 0
        for restante in splitted:
            if restante not in lst:
                id_lst += 1
                id_str = str(id_lst)
                lst[id_str] = self.possibles_combinations(tarefa, restante)

        # agora eu adiciono as regras
        id = 0
        for q in tarefas:
            id += 1
            id_lst += 1
            id_str = str(id_lst)
            lst_bkp = {}
            lst_bkp['1'] = str(q)
            lst[id_str] = lst_bkp
            lista_combinacoes[str(id)] = lst


        # Gero as combinações para os avulsos

        print(lst)

        # Agora vamos tratar das combinações dos elementos
        '''for task in reversed(self.tasks):
            print(str(task.cs), end='->')
            for i in range(len(task.relationships)):
                task_rel = self.get_taskbyid(task.relationships[i])
                print(task_rel.cs, end=',')

                # Pegamos o primeiro elemento e geramos as combinações possíveis
                print('\nGerando as combinações para o elemento: ', end='\n')
                self.possibles_combinations(task_rel.cs)
                print('\n')

            print('')
        '''
        return lst


    def leitura_arvore(self, no):
        if (len(no.relationships) == 0):
            return no

        lst_relationships = [k for k in range(0, len(no.relationships)) if no.relationships[k].visited == False][0]
        self.tasks[lst_relationships] = True
        selected = self.tasks[lst_relationships]
        return self.leitura_arvore(selected)

    def get_first_or(self):
        for k in range(0, len(self.tasks)):
            if self.tasks[k].legend == 'or':
                return self.tasks[k]
        return self.tasks[1]

    def get_taskbyid(self, id):
        for task in self.tasks:
            if task.id == id:
                return task


    def depende_de_alguem(self, elem):
        for k in range(0, len(self.dependences)):
            task = self.dependences[k].cs
            lado_esq = task[0]
            lado_dir = task[1]
            if lado_esq == elem:
                return True

        return False

    def possibles_combinations(self, task, elem):
        combinations = {}
        id = 0
        #if task.legend == 'or' or task.legend == 'paralell':
        if self.depende_de_alguem(elem) == False or (self.depende_de_alguem(elem) == True and elem in self.executados):
                # Adiciono o elemento isolado que ele pode fazer
            combinations['1'] = elem
            # Adiciono agora o elemento em paralelo que ele pode fazer
            combinations['2'] = Functions.parallel(elem)

        return combinations

        '''
        combinations = []
        comb = ''
        id = 0
        for elem in task:
            id += 1
            sp = elem.split(',')[0]
            comb = comb + ',' + sp
            combinations.append(sp)
            combinations.append(Functions.parallel(sp))
            if comb not in combinations and comb != '':
                if comb[0] == ',':
                    comb = comb[1:]
                combinations.append(comb)

        print(combinations)
        '''