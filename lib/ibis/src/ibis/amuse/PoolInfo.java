package ibis.amuse;

import java.io.IOException;
import java.net.InetAddress;
import java.util.Arrays;
import java.util.Properties;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ibis.ipl.Ibis;
import ibis.ipl.IbisCapabilities;
import ibis.ipl.IbisFactory;
import ibis.ipl.IbisIdentifier;
import ibis.ipl.IbisProperties;
import ibis.ipl.PortType;

/**
 * Keeps track of companion Ibisses of a parallel MPI code. Needed to initialize
 * MPI properly.
 * 
 * @author Niels Drost
 * 
 */
public class PoolInfo {

    private static class Shutdown extends Thread {
        private final Ibis ibis;

        Shutdown(Ibis ibis) {
            this.ibis = ibis;
        }

        public void run() {
            try {
                ibis.end();
            } catch (IOException e) {
                logger.error("Error ending PoolInfo");
            }
        }
    }

    private static final Logger logger = LoggerFactory
            .getLogger(PoolInfo.class);

    private final Ibis ibis;

    private final IbisIdentifier[] pool;
    private final String[] hostnames;
    private final int rank;

    public static IbisCapabilities ibisCapabilities = new IbisCapabilities(
            IbisCapabilities.ELECTIONS_STRICT,
            IbisCapabilities.MEMBERSHIP_TOTALLY_ORDERED,
            IbisCapabilities.TERMINATION, IbisCapabilities.SIGNALS,
            IbisCapabilities.CLOSED_WORLD);

    PoolInfo(String poolID, int poolSize) throws Exception {
        Properties properties = new Properties();

        properties.setProperty(IbisProperties.POOL_NAME, poolID);
        properties.setProperty(IbisProperties.POOL_SIZE,
                Integer.toString(poolSize));

        String host = InetAddress.getLocalHost().getHostAddress();

        ibis = IbisFactory.createIbis(ibisCapabilities, properties, true, null,
                null, host, new PortType[0]);
        
        //end ibis when shutdown
        Runtime.getRuntime().addShutdownHook(new Shutdown(ibis));

        logger.info("initializing poolinfo, waiting for others");

        ibis.registry().waitUntilPoolClosed();

        pool = ibis.registry().joinedIbises();

        hostnames = new String[pool.length];

        int rank = 0;
        for (int i = 0; i < hostnames.length; i++) {
            hostnames[i] = pool[i].tagAsString();

            if (ibis.identifier().equals(pool[i])) {
                rank = i;
            }
        }
        this.rank = rank;
        
        logger.info("initialized poolinfo. Hosts: " + Arrays.toString(hostnames));
    }

    public String[] getHostnames() {
        return hostnames;
    }

    public void terminate() {
        try {
            ibis.registry().terminate();
        } catch (IOException e) {
            logger.error("Could not terminate poolinfo pool", e);
        }
    }

    public void waitUntilTerminated() {
        ibis.registry().waitUntilTerminated();
    }

    public int getRank() {
        return rank;
    }

    public void end() throws IOException {
        ibis.end();
    }
}