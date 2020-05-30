# Start from the latest golang base image
FROM golang:latest

LABEL maintainer="Bob Jacobs <bobjac@microsoft.com>"

# Set the current working directory inside the container to the /app directory
WORKDIR /app

# Copy go mode and sum files
COPY go.mod go.sum ./

# Download all dependencies
RUN go mod download

# Copy the source from the current directory
COPY . . 

# Run the go app
RUN go build -o aadpodidentitydemo .

# Expose port 8080
EXPOSE 8080

# Command to run the exec
CMD ["./aadpodidentitydemo -subscriptionid <SUBSCRIPTIONID> -clientid <CLIENTID> -resourcegroup <RESOURCEGROUP>"]

