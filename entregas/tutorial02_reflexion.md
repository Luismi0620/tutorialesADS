# Tutorial 02 - Reflexión

`OrdenBuilder` reduce el riesgo de errores porque concentra los valores por defecto,
las validaciones y el cálculo del total en un único lugar. La interfaz fluida hace
explícitos los datos que se agregan a la orden y evita que cada vista o servicio
repita un constructor largo con argumentos en un orden fácil de confundir. Además,
el Builder se reinicia después de crear cada orden, por lo que no arrastra datos de
una compra anterior.
