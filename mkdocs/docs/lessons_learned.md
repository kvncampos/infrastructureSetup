
# Lessons Learned: Network Configuration Issues

This document outlines lessons learned from two critical issues encountered during the deployment and configuration of a Dockerized HAProxy load balancer and associated services. These insights aim to help avoid similar mistakes in future projects.

---

## Incident Overview

1. **Accidentally Terminating SSH Without Verifying Access**:
    The SSH session was prematurely closed before testing firewall rules, resulting in locked-out access.

2. **Opening a Large Port Range (60000-65000)**:
    Opening this range conflicted with Docker's networking stack, causing the server to become unresponsive and preventing SSH access. This rendered the HAProxy component non-operational.

---

## Mistake 1: Accidental SSH Disconnection

### What Happened
The SSH session was closed before validating connectivity, preventing re-access to the server after firewall changes.

### How to Prevent This
1. **Verify Port Ranges and Limitation**:
    - Verify the port ranges are correct and pick services that best accommodate the requirements.

2. **Validate Access Before Exiting**:
    - Test SSH connectivity from a separate session after applying firewall rules.
    - Keep at least one SSH session active until all configurations are verified.

3. **Enable Recovery Options**:
    - **Console Access**: Ensure cloud console access (e.g., AWS EC2) is available.
    - **Backup SSH Access**: Allow a trusted IP range:
        ```bash
        sudo ufw allow from <trusted_ip> to any port 22
        ```
        - Backup/Recovery Account

4. **Automate Recovery**:
    - Use AWS Systems Manager or equivalent tools to ensure an out-of-band recovery mechanism.

5. **Remove Public Access Last**:
    - Only remove public access after verifying internal connectivity is functional.

---

## Mistake 2: Opening Ports 60000-65000

### What Happened
Opening the range `60000-65000` caused conflicts with Docker's networking stack, binding these ports and disrupting critical services like SSH.

### How to Prevent This
1. **Use Minimal Port Ranges**:
    - Instead of large ranges, identify and open only required ports:
        ```yaml
        ports:
        - "60000:60000"
        - "60001:60001"
        ```

2. **Pre-Test Configurations**:
    - Validate all changes in a local or staging environment to identify potential issues.

3. **Ensure SSH Availability**:
    - Monitor critical ports like `22` during testing.
    - Use tools such as `netstat` to check for port conflicts:
        ```bash
        sudo netstat -tuln | grep 22
        ```

4. **Restrict Traffic**:
    - Limit large port ranges to internal traffic:
        ```bash
        sudo ufw allow from 192.168.1.0/24 to any port 60000:60010 proto tcp
        ```

---

## General Lessons for Future Deployments

1. **Plan and Test Incrementally**:
    - Apply changes in small increments, verifying each step before proceeding.
    - Use scripts or playbooks to document and automate changes.

2. **Backup Critical Configurations**:
    - Save copies of firewall rules and Docker configurations before making changes.

3. **Deploy a Jump Host**:
    - Use a bastion host to maintain consistent access even during misconfigurations.

4. **Restrict Exposure**:
    - Open only the ports required for functionality and limit external access to critical resources.

5. **Monitor Changes in Real Time**:
    - Use logging and monitoring tools to track the impact of changes and detect issues early.

---

!!! success "End Result"
    By implementing these practices, future challenges can be handled more effectively, minimizing downtime and ensuring successful deployment.
