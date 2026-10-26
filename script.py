import numpy as np
import pandas as pd


def generar_dataset_saludmas(
    num_registros=1200, semilla=101, nombre_archivo='saludmas_seguros_proyecto2.csv'
):
  """Genera un dataset sintético para el proyecto de SaludMás Seguros

  con variables demográficas, de salud y valores nulos intencionales.
  """
  # 1. Fijamos la semilla aleatoria para garantizar que los resultados sean idénticos siempre
  np.random.seed(semilla)

  # 2. Generación de variables independientes (demografía y hábitos de vida)
  edades = np.random.randint(18, 66, size=num_registros)  # Edades de 18 a 65 años
  sexos = np.random.choice(['femenino', 'masculino'], size=num_registros)

  # IMC con distribución normal acotada (promedio 30, limitado entre 16 y 50)
  imcs = np.round(
      np.random.normal(loc=30, scale=6, size=num_registros).clip(16.0, 50.0), 1
  )

  # Número de hijos con probabilidades realistas en la población
  hijos = np.random.choice(
      [0, 1, 2, 3, 4, 5],
      size=num_registros,
      p=[0.42, 0.28, 0.17, 0.08, 0.03, 0.02],
  )

  regiones = np.random.choice(['norte', 'sur', 'este', 'oeste'], size=num_registros)
  fumadores = np.random.choice(['sí', 'no'], size=num_registros, p=[0.21, 0.79])

  # 3. Modelado de las reglas de negocio para calcular el costo médico anual
  costo_base = 3000
  impacto_edad = (edades**1.35) * 45

  imc_sobre_30 = np.maximum(imcs - 30, 0)
  impacto_imc = np.where(
      imcs >= 30, (imc_sobre_30**1.5) * 380, np.maximum(imcs - 20, 0) * 50
  )

  # Interacción clave: Fumar eleva el costo, y se agrava si la persona tiene obesidad
  impacto_fumador = np.where(
      fumadores == 'sí', 14000 + np.where(imcs >= 30, (imcs - 25) * 650, 0), 0
  )
  impacto_hijos = hijos * 620
  ruido_mercado = np.random.normal(loc=0, scale=1200, size=num_registros)

  # Suma total de los factores con una variación aleatoria natural
  costo_total = (
      costo_base
      + impacto_edad
      + impacto_imc
      + impacto_fumador
      + impacto_hijos
      + ruido_mercado
  )
  costos_finales = np.round(np.maximum(costo_total, 1100.0), 2)

  # 4. Creación del DataFrame estructurado con Pandas
  df = pd.DataFrame({
      'edad': edades,
      'sexo': sexos,
      'imc': imcs,
      'hijos': hijos,
      'region': regiones,
      'fumador': fumadores,
      'costo_medico_anual': costos_finales,
  })

  # 5. Inyección intencional de datos nulos (NaN) para practicar la fase de limpieza
  idx_imc_nulos = np.random.choice(num_registros, size=15, replace=False)
  idx_fumador_nulos = np.random.choice(num_registros, size=10, replace=False)

  df.loc[idx_imc_nulos, 'imc'] = np.nan
  df.loc[idx_fumador_nulos, 'fumador'] = np.nan

  # 6. Guardado del archivo CSV listo para el proyecto
  df.to_csv(nombre_archivo, index=False)
  print(f'¡Dataset generado con éxito y guardado como "{nombre_archivo}"!')
  return df


# Bloque principal para ejecutar la función al correr el script
if __name__ == '__main__':
  df_resultado = generar_dataset_saludmas()