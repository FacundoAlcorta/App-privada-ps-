from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class SignupForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')

class AgregarDisciplinaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    categoria = StringField('Categoria', validators=[DataRequired(), Length(max=100)])
    instructores = StringField('Nombre instructo/es', validators=[DataRequired(), Length(max=100)])
    '''
    instructores = SelectField(
        'Nombre instructo/es',
        [DataRequired()],
        choices=[
            ('Entrenador 1', 'Entrenador 1'),
            ('Entrenador 2', 'Entrenador 2'),
            ('Entrenador 3', 'Entrenador 3'),
            ('Entrenador 4', 'Entrenador 4'),
            ('Entrenador 5', 'Entrenador 5'),
            ('Entrenador 6', 'Entrenador 6')
        ]
    )
    '''
    dias = StringField('Dias', validators=[DataRequired(), Length(max=64)])
    horario = StringField('Horario', validators=[DataRequired(), Length(max=64)])
    costo_mensual = IntegerField('Costo mensual', validators=[DataRequired(), NumberRange(min=0, max=10000)])
    #habilitada = BooleanField('Habilitada')
    submit = SubmitField('Agregar disciplina')


class AgregarSocioForm(FlaskForm):
    nombre          = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    apellido        = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    tipo_documento  = StringField('Tipo Documento', validators=[DataRequired(), Length(max=64)])
    documento       = IntegerField('Documento', validators=[DataRequired(), NumberRange(min=8, max=64)])
    genero          = StringField('Género', validators=[DataRequired(), Length(max=64)])
    direccion       = StringField('Dirección', validators=[DataRequired(), Length(max=64)])
    telefono        = StringField('Teléfono', validators=[Length(max=25)])
    email           = StringField('Email (Opcional)', validators=[Optional(),Length(max=64), Email()])
    submit          = SubmitField('Agregar Socio')

class AgregarPersonalForm(FlaskForm):
    nombre          = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    apellido        = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    email           = StringField('Email', validators=[DataRequired(), Email()])
    password        = PasswordField('Password', validators=[DataRequired()])
    rol_id          = SelectField('Rol',[DataRequired()],
                        choices=[
                            ('1', 'Administrador'),
                            ('2', 'Operador')
                        ])
    submit          = SubmitField('Agregar Personal')


class ModificarSocioForm(FlaskForm):
    nombre          = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    apellido        = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    tipo_documento  = StringField('Tipo Documento', validators=[DataRequired(), Length(max=64)])
    documento       = IntegerField('Documento', validators=[DataRequired(), NumberRange(min=8, max=64)])
    genero          = StringField('Género', validators=[DataRequired(), Length(max=64)])
    direccion       = StringField('Dirección', validators=[DataRequired(), Length(max=64)])
    telefono        = StringField('Teléfono', validators=[Length(max=25)])
    email           = StringField('Email(Opcional)', validators=[Optional(), Length(max=64), Email()])
    submit          = SubmitField('Modificar Socio')

class ModificarPersonalForm(FlaskForm):
    nombre          = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    apellido        = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    email           = StringField('Email', validators=[Length(max=64), Email()])
    rol_id          = SelectField('Rol',[DataRequired()],
                        choices=[
                            ('1', 'Administrador'),
                            ('2', 'Operador')
                        ])
    submit          = SubmitField('Modificar Personal')

class ModificarDisciplinaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    categoria = StringField('Categoria', validators=[DataRequired(), Length(max=100)])
    instructores = StringField('Nombre instructo/es', validators=[DataRequired(), Length(max=100)])
    dias = StringField('Dias', validators=[DataRequired(), Length(max=64)])
    horario = StringField('Horario', validators=[DataRequired(), Length(max=64)])
    costo_mensual = IntegerField('Costo mensual', validators=[DataRequired(), NumberRange(min=0, max=100000)])
    #habilitada = BooleanField('Habilitada')
    submit = SubmitField('Modificar disciplina')