from rest_framework import serializers
from estudiantes.models import NivelEducativo, Grado, CicloEscolar, Grupo, Estudiante
from .models import (
    ProgramaEducativo, Materia, PeriodoEvaluacion, Maestro, 
    AdministradorEscolar, AsignacionMaestro, Calificacion, 
    CalificacionFinal, AutorizacionCambioCalificacion
)
from users.models import User

# --- Base ---

class NivelEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelEducativo
        fields = ['id', 'nombre', 'orden']

class GradoSerializer(serializers.ModelSerializer):
    nivel_educativo_nombre = serializers.CharField(source='nivel_educativo.nombre', read_only=True)
    
    class Meta:
        model = Grado
        fields = ['id', 'nombre', 'numero_grado', 'nivel_educativo', 'nivel_educativo_nombre']

class CicloEscolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CicloEscolar
        fields = ['id', 'nombre', 'fecha_inicio', 'fecha_fin', 'activo']

class ProgramaEducativoSerializer(serializers.ModelSerializer):
    nivel_educativo = NivelEducativoSerializer(read_only=True)
    
    class Meta:
        model = ProgramaEducativo
        fields = '__all__'

# --- Materias ---

class MateriaSerializer(serializers.ModelSerializer):
    grado = GradoSerializer(read_only=True)
    grado_id = serializers.PrimaryKeyRelatedField(queryset=Grado.objects.all(), source='grado', write_only=True)
    programa_educativo = ProgramaEducativoSerializer(read_only=True)
    programa_educativo_id = serializers.PrimaryKeyRelatedField(queryset=ProgramaEducativo.objects.all(), source='programa_educativo', write_only=True)
    
    num_asignaciones = serializers.IntegerField(read_only=True)

    class Meta:
        model = Materia
        fields = [
            'id', 'nombre', 'clave', 'descripcion', 'creditos', 'orden',
            'activa', 'created_at', 'updated_at',
            'grado', 'grado_id', 'programa_educativo', 'programa_educativo_id',
            'num_asignaciones'
        ]
        read_only_fields = ['clave', 'created_at', 'updated_at']

    def validate_grado_id(self, value):
        user = self.context['request'].user
        if not user.is_superuser:
            try:
                admin = user.admin_escolar_perfil
                if value.nivel_educativo != admin.nivel_educativo:
                    raise serializers.ValidationError("El grado no pertenece a su nivel educativo.")
            except AttributeError:
                pass 
        return value

# --- Maestros ---

class MaestroSerializer(serializers.ModelSerializer):
    usuario_email = serializers.EmailField(source='usuario.email', read_only=True)
    nivel_educativo = NivelEducativoSerializer(read_only=True)
    num_asignaciones = serializers.IntegerField(read_only=True)
    nombre_completo = serializers.SerializerMethodField()
    materias_imparte = serializers.SerializerMethodField()

    class Meta:
        model = Maestro
        fields = [
            'id', 'nombre', 'apellido_paterno', 'apellido_materno', 'nombre_completo',
            'telefono', 'fecha_contratacion', 'activo', 
            'usuario', 'usuario_email', 'nivel_educativo', 
            'num_asignaciones', 'materias_imparte'
        ]

    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"

    def get_materias_imparte(self, obj):
        return list(obj.asignaciones.filter(activa=True).values_list('materia__nombre', flat=True).distinct())

# --- Grupos Simple ---

class GrupoSimpleSerializer(serializers.ModelSerializer):
    grado = GradoSerializer(read_only=True)
    ciclo_escolar = CicloEscolarSerializer(read_only=True)

    class Meta:
        model = Grupo
        fields = [
            'id', 'nombre', 'descripcion', 'capacidad_maxima', 'grado', 'ciclo_escolar'
        ]

# --- Asignaciones ---

class AsignacionMaestroSerializer(serializers.ModelSerializer):
    maestro = MaestroSerializer(read_only=True)
    maestro_id = serializers.PrimaryKeyRelatedField(queryset=Maestro.objects.all(), source='maestro', write_only=True)
    
    grupo = GrupoSimpleSerializer(read_only=True)
    grupo_id = serializers.PrimaryKeyRelatedField(queryset=Grupo.objects.all(), source='grupo', write_only=True)
    
    materia = MateriaSerializer(read_only=True)
    materia_id = serializers.PrimaryKeyRelatedField(queryset=Materia.objects.all(), source='materia', write_only=True)
    
    ciclo_escolar = CicloEscolarSerializer(read_only=True)
    ciclo_escolar_id = serializers.PrimaryKeyRelatedField(queryset=CicloEscolar.objects.all(), source='ciclo_escolar', write_only=True)
    
    grupo_nombre = serializers.CharField(source='grupo.nombre', read_only=True)
    grupo_grado = serializers.CharField(source='grupo.grado.nombre', read_only=True)
    
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)
    materia_clave = serializers.CharField(source='materia.clave', read_only=True)
    
    ciclo_nombre = serializers.CharField(source='ciclo_escolar.nombre', read_only=True)
    
    num_estudiantes = serializers.IntegerField(read_only=True)
    num_calificaciones = serializers.IntegerField(read_only=True)
    avance_captura = serializers.SerializerMethodField()

    class Meta:
        model = AsignacionMaestro
        fields = [
            'id', 'fecha_asignacion', 'activa',
            'maestro', 'maestro_id', 
            'grupo', 'grupo_id', 'grupo_nombre', 'grupo_grado',
            'materia', 'materia_id', 'materia_nombre', 'materia_clave',
            'ciclo_escolar', 'ciclo_escolar_id', 'ciclo_nombre',
            'num_estudiantes', 'num_calificaciones', 'avance_captura'
        ]

    def get_avance_captura(self, obj):
        try:
             total = getattr(obj, 'num_estudiantes', 0)
             capturadas = getattr(obj, 'num_calificaciones', 0)
             if total > 0:
                 return round((capturadas / total) * 100, 2)
             return 0.0
        except Exception:
             return 0.0

# --- Grupos Completo ---

class GrupoSerializer(serializers.ModelSerializer):
    grado = GradoSerializer(read_only=True)
    ciclo_escolar = CicloEscolarSerializer(read_only=True)
    num_estudiantes = serializers.IntegerField(read_only=True)
    num_materias = serializers.IntegerField(read_only=True)
    asignaciones = serializers.SerializerMethodField()

    class Meta:
        model = Grupo
        fields = [
            'id', 'nombre', 'descripcion', 'capacidad_maxima', 'fecha_creacion',
            'grado', 'ciclo_escolar', 'generacion',
            'num_estudiantes', 'num_materias', 'asignaciones'
        ]

    def get_asignaciones(self, obj):
        asignaciones_qs = obj.asignaciones_maestro.filter(activa=True)
        # Aquí usamos el serializer que ya no tiene recursividad hacia Grupo (usa GrupoSimple)
        # O mejor aún, una versión de AsignacionMaestro sin el campo grupo para ahorrar datos
        return AsignacionMaestroSerializer(asignaciones_qs, many=True).data

# --- Periodos ---

class PeriodoEvaluacionSerializer(serializers.ModelSerializer):
    ciclo_escolar_nombre = serializers.CharField(source='ciclo_escolar.nombre', read_only=True)
    dias_restantes = serializers.SerializerMethodField()

    class Meta:
        model = PeriodoEvaluacion
        fields = '__all__'
        read_only_fields = ['fecha_inicio_captura', 'fecha_fin_captura']

    def get_dias_restantes(self, obj):
        from datetime import date
        today = date.today()
        if today <= obj.fecha_fin_captura:
            delta = obj.fecha_fin_captura - today
            return delta.days
        return 0

# --- Calificaciones ---

class EstudianteSimpleSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Estudiante
        fields = ['matricula', 'nombre', 'apellido_paterno', 'apellido_materno', 'nombre_completo', 'curp']
        
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}"

class CalificacionSerializer(serializers.ModelSerializer):
    estudiante = EstudianteSimpleSerializer(read_only=True)
    estudiante_id = serializers.PrimaryKeyRelatedField(queryset=Estudiante.objects.all(), source='estudiante', write_only=True)
    
    periodo_nombre = serializers.CharField(source='periodo_evaluacion.nombre', read_only=True)
    asignacion_materia = serializers.CharField(source='asignacion_maestro.materia.nombre', read_only=True)
    capturada_por_nombre = serializers.CharField(source='capturada_por.nombre_completo', read_only=True)

    class Meta:
        model = Calificacion
        fields = [
            'id', 'calificacion', 'puede_modificar', 'fecha_captura', 'fecha_ultima_modificacion',
            'estudiante', 'estudiante_id', 
            'asignacion_maestro', 'asignacion_materia',
            'periodo_evaluacion', 'periodo_nombre',
            'capturada_por', 'capturada_por_nombre', 'modificada_por', 'autorizada_por'
        ]
        read_only_fields = ['fecha_captura', 'capturada_por', 'modificada_por', 'autorizada_por']

class AutorizacionCambioSerializer(serializers.ModelSerializer):
    calificacion_detalle = CalificacionSerializer(source='calificacion', read_only=True)
    autorizado_por_nombre = serializers.CharField(source='autorizado_por.nombre', read_only=True)

    class Meta:
        model = AutorizacionCambioCalificacion
        fields = '__all__'
