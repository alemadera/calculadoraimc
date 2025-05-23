import os
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from streamlit.runtime.scriptrunner import get_script_run_ctx

# Configuración compatible con versiones recientes
os.environ["STREAMLIT_SERVER_RUN_ON_SAVE"] = "false"
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

def clasificar_grasa(sexo, edad, grasa):
    # Los rangos de grasa varían según el sexo
    if sexo == "Femenino":
        tabla = [(20, 39, [21, 33, 39]), (40, 59, [23, 33.9, 40]), (60, 79, [24, 35.9, 42])]
    else:  # Masculino
        tabla = [(20, 39, [8, 19.9, 25]), (40, 59, [11, 21.9, 30]), (60, 79, [13, 24.9, 35])]

    for rango in tabla:
        if rango[0] <= edad <= rango[1]:
            if grasa < rango[2][0]:
                return "Bajo"
            elif grasa <= rango[2][1]:
                return "Normal"
            elif grasa <= rango[2][2]:
                return "Elevado"
            else:
                return "Muy Elevado"
    return "Fuera de rango"

def clasificar_musculo(sexo, edad, musculo):
    # Los rangos de músculo varían según el sexo
    if sexo == "Femenino":
        tabla = [(18, 39, [24.3, 30.3, 35.4]), (40, 59, [24.1, 30.1, 35.2]), (60, 80, [23.9, 29.9, 34.9])]
    else:  # Masculino
        tabla = [(18, 39, [33.3, 39.3, 43.5]), (40, 59, [33.1, 39.1, 43.3]), (60, 80, [32.9, 38.9, 43.7])]

    for rango in tabla:
        if rango[0] <= edad <= rango[1]:
            if musculo < rango[2][0]:
                return "Bajo"
            elif musculo <= rango[2][1]:
                return "Normal"
            elif musculo <= rango[2][2]:
                return "Elevado"
            else:
                return "Muy Elevado"
    return "Fuera de rango"

def clasificar_imc(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 24.9:
        return "Normal"
    elif imc < 29.9:
        return "Sobrepeso"
    elif imc < 34.9:
        return "Obesidad tipo I"
    elif imc < 39.9:
        return "Obesidad tipo II"
    else:
        return "Obesidad tipo III"

def clasificar_grasa_visceral(grasa_visceral):
    if grasa_visceral < 9:
        return "Normal"
    elif 9.1 <= grasa_visceral <= 14.9:
        return "Alto"
    else:
        return "Muy Alto"

def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)

def calcular_peso_ideal(altura):
    # IMC normal es entre 18.5 y 24.9, calculamos el rango de peso
    imc_min = 18.5
    imc_max = 24.9
    peso_min = round(imc_min * (altura ** 2), 2)
    peso_max = round(imc_max * (altura ** 2), 2)
    return peso_min, peso_max

def get_grasa_normal(sexo, edad):
    # Rango de grasa normal según edad y sexo
    if sexo == "Femenino":
        if 20 <= edad <= 39:
            return "21-33%"
        elif 40 <= edad <= 59:
            return "23-33.9%"
        elif 60 <= edad <= 79:
            return "24-35.9%"
    else:  # Masculino
        if 20 <= edad <= 39:
            return "8-19.9%"
        elif 40 <= edad <= 59:
            return "11-21.9%"
        elif 60 <= edad <= 79:
            return "13-24.9%"

def get_musculo_normal(sexo, edad):
    # Rango de músculo normal según edad y sexo
    if sexo == "Femenino":
        if 18 <= edad <= 39:
            return "24.3-30.3%"
        elif 40 <= edad <= 59:
            return "24.1-30.1%"
        elif 60 <= edad <= 80:
            return "23.9-29.9%"
    else:  # Masculino
        if 18 <= edad <= 39:
            return "33.3-39.3%"
        elif 40 <= edad <= 59:
            return "33.1-39.1%"
        elif 60 <= edad <= 80:
            return "32.9-38.9%"

def mostrar_dashboard():
# Establece la configuración de la página
    st.set_page_config(page_title="Calculadora de Composición Corporal", layout="centered")

    st.markdown(
        """
        <style>
            .col1-padding {
                align-items: center;
            }
        .main .block-container {
            width: 80% !important;  /* Ajusta el ancho de la página */
            max-width: 900px !important;  /* Establece el ancho máximo de la página */
            margin: 0 auto;  /* Centra el contenido */
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(
        """
        <style>
            body {
                                align-items: center;     /* Centrado horizontal */

            }
            h1 {
                text-align: center;
            }
            .column2-content {
                display: flex;
                flex-direction: column;
                justify-content: center; /* Centrado vertical */
                align-items: center;     /* Centrado horizontal */
                height: 100%;            /* Asegura que la columna tenga el mismo alto que la columna 1 */
                text-align: center;      /* Centra el texto */
                padding: 10px;           /* Agrega algo de espacio alrededor */
            }
            .column2 {
                display: flex;
                flex-direction: column;
                align-items: center;     /* Centrado horizontal */
                height: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.title("Calculadora de Composición Corporal")
    
    col1, col2 = st.columns([0.5, 0.5], gap="small")
    
    with col1:
        st.markdown('<div class="col1-padding">', unsafe_allow_html=True)
        nombre = st.text_input("Nombre del Paciente")
        sexo = st.radio("Sexo", ["Femenino", "Masculino"], index=0, horizontal=True)
        edad = st.number_input("Edad", min_value=18, max_value=80)
        altura = st.number_input("Altura (m)", min_value=1.0, max_value=2.5)
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0)
        grasa = st.number_input("% Grasa", min_value=5.0, max_value=70.0)
        musculo = st.number_input("% Músculo", min_value=20.0, max_value=60.0)
        grasa_visceral = st.number_input("Grasa Visceral", min_value=1.0, max_value=30.0)
        st.markdown('</div>', unsafe_allow_html=True)  # Cierra la etiqueta del div con padding
    
    if st.button("Calcular"):
        imc = calcular_imc(peso, altura)
        clasificacion_imc = clasificar_imc(imc)
        clasificacion_grasa = clasificar_grasa(sexo, edad, grasa)
        clasificacion_musculo = clasificar_musculo(sexo, edad, musculo)
        clasificacion_grasa_visceral = clasificar_grasa_visceral(grasa_visceral)
        peso_ideal_min, peso_ideal_max = calcular_peso_ideal(altura)
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        peso_grasa = round((grasa / 100) * peso, 2)
        peso_musculo = round((musculo / 100) * peso, 2)

        
        # Aquí se asegura que esté correctamente indentado dentro de 'with col2:'
        with col2:
            # Contenido centrado dentro de la columna 2
            st.markdown(
                f"""
                <div class="column2">
                    <div class="column2-content">
                        <h3>Resultados</h3>
                        <p><b>IMC:</b><br> {imc} ({clasificacion_imc})<br><i>Rango normal: 18.5 - 24.9</i><br><i>Peso ideal: {peso_ideal_min} kg - {peso_ideal_max} kg</i></p>
                        <p><b>Clasificación de Grasa Corporal:</b><br> {clasificacion_grasa}<br><i>Rango normal: {get_grasa_normal(sexo, edad)}</i></p>
                        <p><b>Clasificación de Músculo:</b><br> {clasificacion_musculo}<br><i>Rango normal: {get_musculo_normal(sexo, edad)}</i></p>
                        <p><b>Índice de Grasa Visceral:</b><br> {grasa_visceral} ({clasificacion_grasa_visceral})<br><i>Rango normal: Menos de 9</i></p>
                        <br>
                        <h4>Resumen</h4>
                        <p>Fecha: {fecha_actual}<br>
                            Paciente: {nombre}<br>
                            IMC: {imc} ({clasificacion_imc})<br>
                            % Grasa: {grasa} ({clasificacion_grasa}) - <b>Peso de grasa:</b> {peso_grasa} kg<br>
                            % Músculo: {musculo} ({clasificacion_musculo}) - <b>Peso de músculo:</b> {peso_musculo} kg<br>
                            Grasa Visceral: {grasa_visceral} ({clasificacion_grasa_visceral})
                        </p>

                    </div>
                </div>
                """, unsafe_allow_html=True
            )
        # Detectar el tema (oscuro o claro) mediante JavaScript y modificar el color
        st.markdown(
            """
            <script>
                // Detectar si el tema del sistema es oscuro
                const isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
                // Cambiar el color del texto en función del tema
                const textColor = isDarkMode ? "white" : "black";

                // Usar este color en los gráficos Plotly
                window.addEventListener('load', function() {
                    const plotlyGraphs = document.querySelectorAll('.stPlotlyChart');
                    plotlyGraphs.forEach(function(graph) {
                        const plotlyElement = graph.querySelector('div');
                        plotlyElement.style.setProperty('--text-color', textColor);
                    });
                });
            </script>
            """, unsafe_allow_html=True)
        st.markdown("---")
        st.write("### Resultados gráficos")
        
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)
        
        def crear_medidor(titulo, valor, rango, clasificacion):
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=valor,
                title={"text": titulo, "font": {"size": 40, "color": "black"}},
                number={"suffix": f"\n<br>{clasificacion}", "font": {"size": 30, "color": "black"}},
                gauge={
                    "axis": {"range": rango},
                    "bar": {"color": "black", "line": {"color": "white", "width": 1.5}},
                    "steps": [
                        {"range": [rango[0], rango[1] * 0.2], "color": "blue"},
                        {"range": [rango[1] * 0.2, rango[1] * 0.4], "color": "green"},
                        {"range": [rango[1] * 0.4, rango[1] * 0.6], "color": "yellow"},
                        {"range": [rango[1] * 0.6, rango[1] * 0.8], "color": "orange"},
                        {"range": [rango[1] * 0.8, rango[1]], "color": "red"}
                    ]
                }
            ))
            return fig
        
        with col3:
            st.plotly_chart(crear_medidor("IMC", imc, [10, 50], clasificacion_imc))
        
        with col4:
            st.plotly_chart(crear_medidor("% Grasa Corporal", grasa, [0, 50], clasificacion_grasa))
        
        with col5:
            st.plotly_chart(crear_medidor("% Músculo", musculo, [20, 60], clasificacion_musculo))
        
        with col6:
            st.plotly_chart(crear_medidor("Grasa Visceral", grasa_visceral, [1, 30], clasificacion_grasa_visceral))

if __name__ == "__main__":
    mostrar_dashboard()


