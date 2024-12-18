# Rate Limiter API

An API to manage and control request limits based on IP addresses. It provides rate-limiting, IP whitelisting/blacklisting, and dynamic configuration updates for rate-limiting thresholds.

## Features

- **Rate Limiting**: Enforces a limit on requests per IP address.
- **IP Management**: Supports adding/removing IPs to/from whitelist and blacklist.
- **Dynamic Configuration**: Allows custom rate-limiting thresholds for specific IPs.
- **Reset Functionality**: Enables resetting limits for specific IPs.

---

## API Endpoints

### **1. Check Rate Limit**
- **Endpoint**: `/rate-limit`
- **Method**: `GET`
- **Description**: Checks if a request is allowed based on the rate-limiting rules.
- **Headers**:
  - `X-Forwarded-For` (string, required): The client's IP address.
- **Responses**:
  - `200 OK`: Request allowed.
    ```json
    {
      "message": "Request allowed."
    }
    ```
  - `429 Too Many Requests`: Rate limit exceeded.
    ```json
    {
      "message": "Too Many Requests. Try again later."
    }
    ```
  - `500 Internal Server Error`: Server error.
    ```json
    {
      "message": "Internal server error"
    }
    ```

---

### **2. Add or Update IP Status**
- **Endpoint**: `/admin/ip-status`
- **Method**: `POST`
- **Description**: Adds or updates the status of an IP address in the whitelist or blacklist.
- **Request Body**:
  ```json
  {
    "ip": "192.168.1.1",
    "status": "whitelist" // Options: "whitelist", "blacklist"
  }
  ```
- **Responses**:
  - `200 OK`: IP status updated successfully.
    ```json
    {
      "message": "IP address status has been updated"
    }
    ```
  - `400 Bad Request`: Invalid input.
    ```json
    {
      "message": "Invalid request. Provide 'ip' and 'status' as 'whitelist' or 'blacklist'."
    }
    ```
  - `500 Internal Server Error`: Server error.
    ```json
    {
      "message": "Internal server error"
    }
    ```

---

### **3. Reset Rate Limit**
- **Endpoint**: `/admin/reset-limit`
- **Method**: `POST`
- **Description**: Resets the rate limit for a specific IP address.
- **Request Body**:
  ```json
  {
    "ip": "192.168.1.1"
  }
  ```
- **Responses**:
  - `200 OK`: Rate limit reset successfully.
    ```json
    {
      "message": "Rate limit has been reset"
    }
    ```
  - `400 Bad Request`: Invalid input.
    ```json
    {
      "message": "Invalid request. Provide 'ip' to reset rate limit"
    }
    ```
  - `500 Internal Server Error`: Server error.
    ```json
    {
      "message": "Internal server error"
    }
    ```

---

### **4. Update Rate Limit Configuration**
- **Endpoint**: `/admin/configuration`
- **Method**: `PUT`
- **Description**: Updates the rate-limiting configuration (threshold and time window) for a specific IP.
- **Request Body**:
  ```json
  {
    "ip": "192.168.1.1",
    "threshold": 100,        // Maximum allowed requests
    "time_window": 3600      // Time window in seconds
  }
  ```
- **Responses**:
  - `200 OK`: Configuration updated successfully.
    ```json
    {
      "message": "Configuration updated successfully"
    }
    ```
  - `400 Bad Request`: Invalid input.
    ```json
    {
      "message": "Invalid request. Provide 'ip', 'threshold', and 'time_window'."
    }
    ```
  - `500 Internal Server Error`: Server error.
    ```json
    {
      "message": "Internal server error"
    }
    ```

---

## Testing

### **Unit Tests**
Run unit tests to validate functionality:
```bash
pytest
```

### **Postman Testing**
Import the [Swagger YAML](./swagger.yml) into Postman for testing.

---

## Deployment

Deploy the application to AWS using the Serverless Framework:
```bash
serverless deploy
```

---

## Notes
- Use the `admin` endpoints to manage IPs and configurations dynamically.
