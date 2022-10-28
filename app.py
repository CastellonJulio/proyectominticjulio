from datetime import date, datetime
from flask import Flask, render_template, url_for, request, redirect, flash, session, jsonify
import controlator
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.secret_key='My secret password'+str(datetime.now)

##### RUTAS CAPTURA DE DATOS #######

@app.route('/cambiarclave', methods=['POST'])
def restablecer_cuenta():
    datos=request.form
    usu=datos['username']
    p1=datos['p1']
    p2=datos['p2']
    p1enc=generate_password_hash(p1)
    if p1==p2:
        resul=controlator.restablecer_cuenta(usu,p1enc)
        if resul:
            flash('Contraseña Actualizada Correctamente')
        else:
            flash('No fue posible Actualizar Correctamente la Contraseña')
    else:
        flash('Contraseñas no coinciden')

    return redirect(url_for('login'))


@app.route('/recuperarcuenta', methods=['POST'])
def recuperar_cuenta():
    datos=request.form
    usu=datos['username']
    resul=controlator.recupera_cuenta(usu)
    if resul=='SI':
        flash('Usuario Encontrado: Mensaje enviado al correo')
    elif resul=='NO':
        flash('Usuario No Existe en la base de datos')
    else:
        flash('No es posible ejecutar la consulta, intentelo más tarde')
    return redirect(url_for('recuperar'))

@app.route('/consultarmail', methods=['GET', 'POST'])
def consulta_mail():
    if request.method=='POST':
        datos=request.get_json()
    else:
        resul=controlator.listar_mensajes(1,'')
    return jsonify(resul)


##mensajes individuales y se optimiza para obtener las dos
@app.route('/listmindivi', methods=['GET','POST'])
def list_msn_indivi():
    if request.method=='POST':

        datos=request.get_json()
        username=datos['username']
        tipo=datos['tipo']
        if tipo==1:
            resul=controlator.listar_mensajes(1,'')
        else:
            resul=controlator.listar_mensajes(2,username)
        return jsonify(resul)
    else:
        resul=controlator.listar_mensajes(1,'')
        return jsonify(resul)

    

## lista de mensajes en formato json
@app.route('/listarmensaje')
def listar_mensajes():
    #datos=request.get_json():
    resul=controlator.listar_mensajes(1,'')
    return jsonify(resul)

## lista de usuarios en formato json
@app.route('/listarusuarios')
def listar_g_usuarios():
    #datos=request.get_json():
    resul=controlator.listar_g_usuarios()
    return jsonify(resul)


@app.route('/consultamensajes')
def consulta_mensajes():
    #usu='juliocastellonmendozaqgmail.com'
    resul=controlator.listar_mensaje()
    return jsonify(resul)

@app.route('/consultamensajesind', methods=['POST'])
def consulta_mensajes_ind():
    datos=request.get_json()
    usu=datos['username']
    resul=controlator.listar_mensaje(usu)
    return jsonify(resul)

@app.route('/enviarmensaje', methods=['POST'])
def enviar_mensaje():
    datos=request.form
    rem=session['username']
    dest=datos['destinatario']
    asu=datos['asunto']
    mens=datos['cuerpo']
    resul=controlator.adicionar_mensaje(rem,dest,asu,mens)
    if resul:
        flash('Mensaje envíado exitosamente')
    else:
        flash('Error al envíar mensaje')

    listadouser=controlator.listar_usuario(rem)
    return render_template('mensajeria.html',datauser=listadouser)
    #return redirect(url_for('mensajeria'))


@app.route('/activarcuenta', methods=['POST'])
def activar_cuenta():
    datos=request.form
    usu=datos['usuario']
    cod_v=datos['codverifi']
    resultado=controlator.activar_cuenta(usu,cod_v)
    if resultado:
        flash('Cuenta Activada Satisfactoriamente')
    else:
        flash('Error en la Activación')
    return redirect(url_for('validar'))


@app.route('/validarlogin', methods=['POST'])
def validar_login():
    datos=request.form
    usu=datos['usuario']
    passw=datos['passw']
                    
    if usu=='' or passw=='':
        flash('Datos Incorrectos')
        
        return redirect(url_for('login'))
    else:
        resultado=controlator.validacion_login(usu)
        if resultado==False:
            flash('Error en consulta')
            
            return redirect(url_for('login'))
        else:
            ## Se usa la Y por que al activarla desde la base de datos me genera Y como valor
            if resultado[0]['verifi']==1 or resultado[0]['verifi']=='Y':
                if check_password_hash(resultado[0]['passw'],passw):
                    ## vector para saber quien esta logeado
                    session['username']=usu
                    session['nombre']=resultado[0]['nombre']+" "+resultado[0]['apellido']
                    listaruser=controlator.listar_usuario(usu)
                    ##pasar lista de los usuarios a la siguiente vista
                    return render_template('mensajeria.html', datauser=listaruser)
                else:
                    flash('Contraseña Incorrecta')
                    
                    return redirect(url_for('login'))
            else:
                    
                    return redirect(url_for('validar'))
        
                ##return redirect(url_for('login'))
    


@app.route('/addregistro', methods=['POST'])
def addregistro():
    datos=request.form
    nom=datos['nombre']
    ape=datos['apellido']
    usu=datos['usuario']
    p1=datos['pass1']
    p2=datos['pass2']

#### Para encriptar el paswwword
    p1enc=generate_password_hash(p1)

    '''
    try:

        poli=datos['poli']
    except:
        flash('Debe aceptar las politicas')
    '''
    
### Validaciones para registrarse
    if nom=='' or ape=='' or usu=='' or p1=='' or p2=='':
        #return '<h2>Datos incompletos</h2>'
        flash('Datos incompletos')
        return redirect(url_for('registro'))
    elif p1 != p2:
        #return '<h2>La s contraseñas no coinciden</h2>'
        flash('Las contraseñas no coinciden')
        return redirect(url_for('registro'))
    elif len(p1)<6:
        #return '<h2>Verificar cantidad de caracteres de la contraseña sea mayor de 6</h2>'
        flash('Verificar cantidad de caracteres de la contraseña, debe sea mayor de 6 digitos')
        return redirect(url_for('registro'))
    else:
        resultado=controlator.add_registro(nom,ape,usu,p1enc)
        print(resultado)
        if resultado:
            flash('Registo Correctamente, verificar en su correo el codigo para la activación de la cuenta')
            return redirect(url_for('registro'))
        else:
            flash('Error en Base de Datos')
            return redirect(url_for('registro'))




##### RUTAS NAVEGACIÓN #######

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login')
def login():
    session.clear()
    return render_template('login.html')


@app.route('/registro')
def registro():
    return render_template('registro.html')


@app.route('/validar')
def validar():
    return render_template('validar.html')

@app.route('/mensajeria')
def mensajeria():
    listadouser=controlator.listar_usuario(session['username'])
    return render_template('mensajeria.html',datauser=listadouser)


@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/restablecer/<usuario>')
@app.route('/restablecer')
def restablecer(usuario=None):
    if usuario:
        return render_template('restablecer.html', userdata=usuario)
    else:
        return render_template('restablecer.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/politicas')
def politicas():
    return render_template('politicas.html')

@app.route('/usuarios')
def menu_user():
    return render_template('usuarios.html')

@app.route('/productos')
def menu_product():
    return render_template('productos.html')

@app.route('/carrito')
def menu_carrito():
    return render_template('carrito.html')

@app.route('/deseos')
def list_deseos():
    return render_template('deseos.html')

@app.route('/gestionProducto')
def gestionProducto():
    return render_template('gestionProducto.html')


@app.before_request
def protegerrutas():
    ruta=request.path
    if not 'username' in session and (ruta=='/menu' or ruta=='/mensajeria'):
        flash('Debe ingresar primero al sistema')
        return redirect('/login')


if __name__=='__main__':
    app.run(debug=True)