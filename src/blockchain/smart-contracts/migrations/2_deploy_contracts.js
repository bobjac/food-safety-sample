var FoodSafety = artifacts.require("FoodSafety");

module.exports = deployer => {
    deployer.deploy(FoodSafety);
};