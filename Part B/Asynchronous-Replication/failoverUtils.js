const queryPrimaryStorageStatus = () => {
    const isHealthy = Math.random() > 0.2;
    return isHealthy ? 'healthy' : 'unhealthy';
};

const initiateFailover = () => {
    console.log('Failover initiated. Switching to secondary storage system...');
};

module.exports = { queryPrimaryStorageStatus, initiateFailover };