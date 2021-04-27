## Background
[mitmproxy](https://mitmproxy.org/) is a free and open source interactive HTTPS proxy. Given that Matt's directory was pulling from a different API, I needed to use mitmproxy to uncover the correct API endpoint for the Mini Leaderboard. 

## Set Up
The set up and walk-through are largely covered in [this Medium article](https://medium.com/testvagrant/intercept-ios-android-network-calls-using-mitmproxy-4d3c94831f62) by Gaurav Sharma. Once connected, it's easy to scope through the post requests and see from which API the leaderboard metrics were being sent from. The only major callout is making sure the user agent is correct, as that caused some headaches initially. 
