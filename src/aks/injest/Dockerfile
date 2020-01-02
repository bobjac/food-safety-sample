FROM mcr.microsoft.com/dotnet/core/runtime:3.1

COPY injest/bin/Release/netcoreapp3.1/publish/ injest/

ENTRYPOINT [ "dotnet", "injest/injest.dll" ]