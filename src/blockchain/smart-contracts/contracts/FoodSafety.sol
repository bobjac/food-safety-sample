pragma solidity ^0.5.0;

contract FoodSafety
{
    struct Record {
        string sensorId;
        int256 temperature;
        int256 humidity;
        string timestamp;
    }

    uint public numRecords;
    Record[] public records;

    address private owner;

     //Set of States
    enum StateType { Compliant, NonCompliant }

    //List of properties
    StateType public  State;

    event StateChanged(string stateData);

    // constructor function
    constructor() public
    {
        owner = msg.sender;
        numRecords = 0;

        emit StateChanged('Request');
    }

    function SetRecord(string memory sensorId, int256 temperature, int256 humidity, string memory timestamp) public
    {
        Record memory r;
        r.sensorId = sensorId;
        r.temperature = temperature;
        r.humidity = humidity;
        r.timestamp = timestamp;
        
        if (isValid(r)) {
            records.push(r);
            numRecords++;
        }
    }
    function isValid(Record memory r) private returns (bool) {
        bool isValid = true;
        int256 minTemp = -50;
        int256 maxTemp = 50;
        int minHumidity = -50;
        int maxHumidity = 50;
        
        if (r.temperature < minTemp || r.temperature > maxTemp) {
            State = StateType.NonCompliant;
            emit StateChanged("HORRIBLE!!!!!!");
            isValid = false;
        }
        
        if (r.humidity < minHumidity || r.humidity > maxHumidity) {
            State = StateType.NonCompliant;
            emit StateChanged("HORRIBLE!!!!!!");
            isValid = false;
        }
        
        return isValid;
    }
    
    function GetRecordCount() public returns (uint) {
        return numRecords;
    }
    
    function GetRecordByIndex(uint index) public returns (string memory, int256, int256, string memory) {
        if (index > numRecords) {
            // throw an error
        }
        
        Record memory r = records[index];
        return (r.sensorId, r.temperature, r.humidity, r.timestamp);
    }
    
    function GetContractState() public returns (StateType) {
        return State;
    }
}