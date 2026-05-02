-- Auto-Naming Script for OBS Studio
-- Renombra archivos de grabación automáticamente
obs = obslua

function script_description()
    return "Auto-Naming Script: Renombra grabaciones con [Título] [Fecha].\n\nSoporte: https://www.paypal.com/donate/?business=ramiro.silva.1993@gmail.com"
end

function script_properties()
    local props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "prefix", "Prefijo del archivo:", obs.OBS_TEXT_DEFAULT)
    return props
end

function script_load(settings)
    obs.script_log(obs.LOG_INFO, "Auto-Naming Script Cargado correctamente.")
end

-- Lógica básica de hook de grabación
function script_update(settings)
    -- Aquí se implementaría la lógica de monitoreo de archivos
end
