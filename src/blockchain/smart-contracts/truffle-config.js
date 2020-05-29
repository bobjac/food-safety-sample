const HDWalletProvider = require("truffle-hdwallet-provider");
const fs = require("fs");
module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*"
    },
    abs_bobjacabstest_bobjacabstest_bobjacabstest: {
      network_id: "*",
      gas: 0,
      gasPrice: 0,
      provider: new HDWalletProvider(fs.readFileSync('/Users/bobjacobs/work/customers/Untitled.env', 'utf-8'), "https://bobjacabstest.blockchain.azure.com:3200/GYX5d3JeeFiNQDF84Ov-rIhm")
    }
  }
};
