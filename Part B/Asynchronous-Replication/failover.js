const { queryPrimaryStorageStatus, initiateFailover } = require('./failoverUtils');

const monitoringInterval = 60000;

const startFailoverMonitoring = () => {
    console.log('Failover monitoring started...');
    setInterval(monitorPrimaryStorage, monitoringInterval);
};

const monitorPrimaryStorage = () => {
    const primaryStatus = queryPrimaryStorageStatus();

    if (primaryStatus === 'healthy') {
        console.log('Primary storage is healthy');
        return;
    }

    console.log('Primary storage is unhealthy, initiating failover...');
    initiateFailover();
};

module.exports = { startFailoverMonitoring };