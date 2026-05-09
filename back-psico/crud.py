"""
Operaciones CRUD para gestionar pacientes y juegos activos
"""
from datetime import datetime
from sqlalchemy.orm import Session
from models import Paciente, JuegoActivo, JuegoActivoTBOI, JuegoActivoMinecraft, Juego,Boss


class GestorPacientes:
    """Gestor de operaciones con pacientes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # CREATE
    def crear_paciente(self, nombre, apellido, **kwargs):
        """Crear un nuevo paciente"""
        paciente = Paciente(
            nombre=nombre,
            apellido=apellido,
            **kwargs
        )
        self.db.add(paciente)
        self.db.commit()
        self.db.refresh(paciente)
        return paciente
    
    # READ
    def obtener_paciente(self, paciente_id):
        """Obtener un paciente por ID"""
        return self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
    
    def obtener_todos_pacientes(self):
        """Listar todos los pacientes"""
        return self.db.query(Paciente).all()
    
    def obtener_pacientes_activos(self):
        """Obtener solo pacientes activos"""
        return self.db.query(Paciente).filter(Paciente.activo == True).all()
    
    def buscar_por_nombre(self, nombre):
        """Buscar pacientes por nombre"""
        return self.db.query(Paciente).filter(Paciente.nombre.ilike(f"%{nombre}%")).all()
    
    # UPDATE
    def actualizar_paciente(self, paciente_id, **kwargs):
        """Actualizar datos de un paciente"""
        paciente = self.obtener_paciente(paciente_id)
        if paciente:
            for key, value in kwargs.items():
                if hasattr(paciente, key) and key != 'juegos_activos':
                    setattr(paciente, key, value)
            self.db.commit()
            self.db.refresh(paciente)
        return paciente
    
    # DELETE
    def desactivar_paciente(self, paciente_id):
        """Desactivar un paciente (borrado lógico)"""
        return self.actualizar_paciente(paciente_id, activo=False)
    
    def eliminar_paciente(self, paciente_id):
        """Eliminar completamente un paciente"""
        paciente = self.obtener_paciente(paciente_id)
        if paciente:
            self.db.delete(paciente)
            self.db.commit()
        return True


class GestorJuegosActivos:
    """Gestor de operaciones con juegos activos de pacientes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # MÉTODOS GENERALES
    def obtener_juego_activo(self, juego_id):
        """Obtener un juego activo por ID (cualquier tipo)"""
        return self.db.query(JuegoActivo).filter(JuegoActivo.id == juego_id).first()
    
    def obtener_todos_juegos_activos(self):
        """Listar todos los juegos activos"""
        return self.db.query(JuegoActivo).all()
    
    def obtener_juegos_activos_por_paciente(self, paciente_id):
        """Obtener todos los juegos activos de un paciente"""
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if paciente:
            return paciente.juegos_activos
        return []
    
    def obtener_juegos_activos_activos(self, paciente_id):
        """Obtener solo los juegos activos (activo=True) de un paciente"""
        juegos = self.obtener_juegos_activos_por_paciente(paciente_id)
        return [j for j in juegos if j.activo]
    
    def actualizar_juego_activo(self, juego_id, **kwargs):
        """Actualizar datos de un juego activo"""
        juego = self.obtener_juego_activo(juego_id)
        if juego:
            for key, value in kwargs.items():
                if hasattr(juego, key) and key != 'pacientes':
                    setattr(juego, key, value)
            self.db.commit()
            self.db.refresh(juego)
        return juego
    
    def desactivar_juego(self, juego_id):
        """Desactivar un juego (marcar como inactivo)"""
        return self.actualizar_juego_activo(juego_id, activo=False, fecha_fin=datetime.utcnow())
    
    def eliminar_juego_activo(self, juego_id):
        """Eliminar completamente un juego activo"""
        juego = self.obtener_juego_activo(juego_id)
        if juego:
            self.db.delete(juego)
            self.db.commit()
        return True
    
    # ASIGNACIÓN DE JUEGOS A PACIENTES
    def asignar_juego_a_paciente(self, paciente_id, juego_id):
        """Asignar un juego activo a un paciente"""
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        juego = self.obtener_juego_activo(juego_id)
        
        if paciente and juego:
            if juego not in paciente.juegos_activos:
                paciente.juegos_activos.append(juego)
                self.db.commit()
                return True
        return False
    
    def desasignar_juego_de_paciente(self, paciente_id, juego_id):
        """Desasignar un juego activo de un paciente"""
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        juego = self.obtener_juego_activo(juego_id)
        
        if paciente and juego:
            if juego in paciente.juegos_activos:
                paciente.juegos_activos.remove(juego)
                self.db.commit()
                return True
        return False
    
    # MÉTODOS ESPECÍFICOS PARA THE BINDING OF ISAAC

    

    def crear_tboi(self, paciente_id, personaje, dificultad, 
                   items_recolectados=None, notas=None,
                   boss_id=None, cronograma_semanal=None, frase_semanal=None,
                   objetivos=None, recompensas=None, corazones=0, keys=0, bombas=0, monedas=0):
        """Crear un nuevo juego de The Binding of Isaac"""
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            return None
        
        juego = JuegoActivoTBOI(
            personaje=personaje,
            dificultad=dificultad,
            items_recolectados=items_recolectados,
            notas=notas,
            boss_id=boss_id,
            cronograma_semanal=cronograma_semanal,
            frase_semanal=frase_semanal,
            objetivos=objetivos,
            recompensas=recompensas,
            corazones=corazones,
            keys=keys,
            bombas=bombas,
            monedas=monedas
        )
        self.db.add(juego)
        self.db.commit()
        self.db.refresh(juego)
        
        paciente.juegos_activos.append(juego)
        self.db.commit()
        
        return juego
    
    def update_tboi_progreso(self, juego_id, progreso_pisos=None, 
                             items=None, logros=None):
        """Actualizar progreso de The Binding of Isaac"""
        juego = self.db.query(JuegoActivoTBOI).filter(JuegoActivoTBOI.id == juego_id).first()
        if juego:
            if progreso_pisos is not None:
                juego.progreso_pisos = progreso_pisos
            if items is not None:
                juego.items_recolectados = items
            if logros is not None:
                juego.logros = logros
            self.db.commit()
            self.db.refresh(juego)
        return juego
    
    def obtener_tboi_por_paciente(self, paciente_id):
        """Obtener todos los juegos de The Binding of Isaac de un paciente"""
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            return []
        return [j for j in paciente.juegos_activos if isinstance(j, JuegoActivoTBOI)]
    
    # MÉTODOS ESPECÍFICOS PARA MINECRAFT
    def crear_minecraft(self, paciente_id, nombre_mundo, modo_juego, 
                       bioma_actual=None, notas=None):
        """Crear un nuevo juego de Minecraft"""
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            return None
        
        juego = JuegoActivoMinecraft(
            nombre_mundo=nombre_mundo,
            modo_juego=modo_juego,
            bioma_actual=bioma_actual,
            notas=notas,
            nivel_experiencia=0,
            tiempo_juego=0,
            bloques_minados=0,
            bloques_colocados=0,
            distancia_caminada=0.0
        )
        self.db.add(juego)
        self.db.commit()
        self.db.refresh(juego)
        
        paciente.juegos_activos.append(juego)
        self.db.commit()
        
        return juego
    
    def update_minecraft_progreso(self, juego_id, nivel_experiencia=None, 
                                  bloques_minados=None, bloques_colocados=None,
                                  distancia_caminada=None, mobs_derrotados=None,
                                  estructuras_encontradas=None, tiempo_juego=None,
                                  bioma_actual=None):
        """Actualizar progreso de Minecraft"""
        juego = self.db.query(JuegoActivoMinecraft).filter(JuegoActivoMinecraft.id == juego_id).first()
        if juego:
            if nivel_experiencia is not None:
                juego.nivel_experiencia = nivel_experiencia
            if bloques_minados is not None:
                juego.bloques_minados = bloques_minados
            if bloques_colocados is not None:
                juego.bloques_colocados = bloques_colocados
            if distancia_caminada is not None:
                juego.distancia_caminada = distancia_caminada
            if mobs_derrotados is not None:
                juego.mobs_derrotados = mobs_derrotados
            if estructuras_encontradas is not None:
                juego.estructuras_encontradas = estructuras_encontradas
            if tiempo_juego is not None:
                juego.tiempo_juego = tiempo_juego
            if bioma_actual is not None:
                juego.bioma_actual = bioma_actual
            self.db.commit()
            self.db.refresh(juego)
        return juego
    
    def obtener_minecraft_por_paciente(self, paciente_id):
        """Obtener todos los juegos de Minecraft de un paciente"""
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            return []
        return [j for j in paciente.juegos_activos if isinstance(j, JuegoActivoMinecraft)]


class GestorBosses:
    """Gestor de operaciones con bosses"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # CREATE
    def crear_boss(self, nombre, dificultad=None, descripcion=None, estrategias=None):
        """Crear un nuevo boss"""
        boss = Boss(
            nombre=nombre,
            dificultad=dificultad,
            descripcion=descripcion,
            estrategias=estrategias
        )
        self.db.add(boss)
        self.db.commit()
        self.db.refresh(boss)
        return boss
    
    # READ
    def obtener_boss(self, boss_id):
        """Obtener un boss por ID"""
        return self.db.query(Boss).filter(Boss.id == boss_id).first()
    
    def obtener_todos_bosses(self):
        """Listar todos los bosses"""
        return self.db.query(Boss).all()
    
    def obtener_boss_por_nombre(self, nombre):
        """Obtener boss por nombre"""
        return self.db.query(Boss).filter(Boss.nombre.ilike(f"%{nombre}%")).first()
    
    # UPDATE
    def actualizar_boss(self, boss_id, **kwargs):
        """Actualizar datos de un boss"""
        boss = self.obtener_boss(boss_id)
        if boss:
            for key, value in kwargs.items():
                if hasattr(boss, key) and value is not None:
                    setattr(boss, key, value)
            self.db.commit()
            self.db.refresh(boss)
        return boss
    
    # DELETE
    def eliminar_boss(self, boss_id):
        """Eliminar un boss"""
        boss = self.obtener_boss(boss_id)
        if boss:
            self.db.delete(boss)
            self.db.commit()
        return boss

