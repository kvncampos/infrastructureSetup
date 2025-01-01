# Lessons Learned: Network Configuration Issues

This document highlights the lessons learned from two critical issues that occurred during the deployment and configuration of a Dockerized HAProxy load balancer and associated services. These issues offer insights into better practices for future implementations.

---

## Incident Overview

1. **Accidentally Terminating SSH Without Verifying Access**:
   The SSH session was prematurely closed before testing if firewall rules allowed access to all servers, resulting in locked-out access.

2. **Opening a Large Port Range (60000-65000)**:
   Opening this range conflicted with Docker's networking stack, effectively "hanging" the server and preventing SSH access. This rendered the HAProxy component non-operational.

---

??? tip "Summary"
    This post mortem emphasizes the importance of careful planning, testing, and monitoring during network configurations. By implementing safeguards such as staged changes, sandbox testing, and limiting exposure, similar issues can be avoided in the future.

## Mistake 1: Accidental SSH Disconnection

### What Happened:
- The SSH session was closed before validating connectivity after firewall rule changes. This prevented re-accessing the server for further configuration.

### What Should Have Been Done:
1. **Validate SSH Access Before Exiting**:
    - Test SSH access from another terminal or session immediately after applying firewall rules.
    - Keep one SSH session open until all configurations are verified.

2. **Implement an SSH Backup Plan**:
    - **Enable Console Access**: Ensure console (e.g., AWS EC2 Console) access is always available for recovery.

    - **Allow a Trusted IP Range**:
     ```bash
     sudo ufw allow from <your_ip> to any port 22
     ```

3. **Automate SSH Recovery**:
    - Use tools like AWS Systems Manager Session Manager to create an out-of-band connection.
    - Configure a separate user account with limited access for recovery purposes.

4. **Remove Public Access Last**:
    - Once you verify SSH is allowed from the designated servers, remove the public access last.

---

## Mistake 2: Opening Ports 60000-65000

### What Happened:
- Opening a large port range caused conflicts with Docker's networking stack, which likely bound these ports. This disrupted the server's SSH functionality and led to a complete loss of access.

### What Should Have Been Done:
1. **Minimize Port Range Usage**:
    - Avoid large ranges like `60000-65000` unless explicitly required.
    - For HAProxy, map fewer, specific ports:
        ```yaml
        ports:
        - "60000-60010:60000-60010"
        ```

2. **Pre-Test in a Sandbox Environment**:
    - Use a local Docker test environment or staging server to validate configurations before applying them to production servers.

3. **Monitor Critical Ports**:
    - Ensure SSH (port 22) remains open at all times during testing.
    - Use tools like `netstat` or `ss` to identify potential port conflicts:
        ```bash
        sudo netstat -tuln
        ```

4. **Understand Production Requirements**:
    - Large port ranges are uncommon in production. If needed, restrict them to internal traffic only:
        ```bash
        sudo ufw allow from 192.168.1.0/24 to any port 60000:65000 proto tcp
        ```
    - Verify the port ranges.
---

## General Lessons for Future Deployments

1. **Plan Firewall Changes with a Dry Run**:
    - Write changes in a script or playbook and validate them interactively before deployment:
        ```bash
        sudo ufw allow 22/tcp
        sudo ufw allow 80/tcp
        sudo ufw allow 60000:60010/tcp
        ```

2. **Create a Disaster Recovery Plan**:
    - **Backup Configuration Files**: Always back up firewall rules and Docker configurations.
    - **Use a Jump Host**: Deploy a dedicated bastion host to ensure access even during misconfigurations.

3. **Restrict Port Exposure**:
    - Only open ports explicitly required for the application.
    - For large ranges, restrict them to internal traffic.

4. **Monitor and Audit Changes**:
    - Use logging and monitoring tools to verify the impact of changes in real-time.
    - Enable audit logging for sensitive configurations.

---

