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
      provider: new HDWalletProvider(fs.readFileSync('/Users/bobjacobs/work/customers/Untitled.env', 'utf-8'), "https://bobjacfoodsafetyt20.blockchain.azure.com:3200/zpauIGYHVNni-AxLQC5ypgLs")
    },
    abs_foodsafetyt20_bobjacfoodsafetyt20_bobjacfoodsafetyt20: {
      network_id: "*",
      gas: 0,
      gasPrice: 0,
      provider: new HDWalletProvider(fs.readFileSync('/Users/bobjacobs/work/customers/Untitled.env', 'utf-8'), "https://bobjacfoodsafetyt20.blockchain.azure.com:3200/zpauIGYHVNni-AxLQC5ypgLs")
    },
    abs_bobjacfoodsafety2_bobjacfoodsafety2_bobjacfoodsafety2: {
      network_id: "*",
      gasPrice: 0,
      provider: new HDWalletProvider(fs.readFileSync('/Users/bobjacobs/work/customers/Untitled.env', 'utf-8'), "https://bobjacfoodsafety2.blockchain.azure.com:3200/aVIVZ9SculsRf1qF7Xhz1unj")
    }
  }
};
