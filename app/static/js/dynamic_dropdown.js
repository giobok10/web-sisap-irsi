document.addEventListener("DOMContentLoaded", function () {
  const paisSelect = document.getElementById("pais");
  const ciudadSelect = document.getElementById("ciudad");

  const ciudadesPorPais = {
    "Guatemala": ["Ciudad de Guatemala", "Quetzaltenango", "Antigua Guatemala"],
    "El Salvador": ["San Salvador", "Santa Ana", "San Miguel"],
    "Honduras": ["Tegucigalpa", "San Pedro Sula", "La Ceiba"],
    "Nicaragua": ["Managua", "León", "Granada"],
    "Costa Rica": ["San José", "Alajuela", "Cartago"],
    "Panamá": ["Ciudad de Panamá", "Colón", "David"],
    "República Dominicana": ["Santo Domingo", "Santiago", "La Romana"],
    "Paraguay": ["Asunción", "Caaguazú", "Misiones"],
    "Colombia": ["Bogotá", "Medellin", "Cali"],
    "México": ["Ciudad de México", "Monterrey", "Guadalajara"]
  };

  function actualizarCiudades(pais) {
    // Limpiar el select de ciudades completamente antes de agregar nuevas
    ciudadSelect.innerHTML = "";

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Seleccione ciudad";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    ciudadSelect.appendChild(defaultOption);

    const ciudades = ciudadesPorPais[pais] || [];

    // Agregar solo las 3 ciudades principales sin duplicar
    new Set(ciudades).forEach(ciudad => {
      const option = document.createElement("option");
      option.value = ciudad;
      option.textContent = ciudad;
      ciudadSelect.appendChild(option);
    });
  }

  paisSelect.addEventListener("change", function () {
    actualizarCiudades(this.value);
  });

  // Cargar ciudades si ya hay un país preseleccionado
  if (paisSelect.value) {
    actualizarCiudades(paisSelect.value);
  }
});
