<?php
header('Content-Type: application/json');

function get_server_cpu_usage() {
    $load = sys_getloadavg();
    return isset($load[0]) ? min(100, round($load[0] * 100 / 4)) : 0;
}

function get_server_memory_usage() {
    $free = shell_exec('wmic OS get FreePhysicalMemory /Value');
    $total = shell_exec('wmic OS get TotalVisibleMemorySize /Value');
    
    $free = trim(str_replace('FreePhysicalMemory=', '', $free));
    $total = trim(str_replace('TotalVisibleMemorySize=', '', $total));
    
    if ($free && $total) {
        $used = $total - $free;
        return round(($used / $total) * 100);
    }
    return 0;
}

function get_network_status() {
    $netstat = shell_exec('netstat -n | find "ESTABLISHED" /c');
    $connections = intval(trim($netstat));
    return min(100, round(($connections / 100) * 100));
}

$metrics = [
    'system_status' => 100,
    'cpu_usage' => get_server_cpu_usage(),
    'memory_usage' => get_server_memory_usage(),
    'network_status' => get_network_status()
];

echo json_encode($metrics);