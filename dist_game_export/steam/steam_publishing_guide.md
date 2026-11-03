# How to Publish MetaHorizon Odyssey 3D to Steam

1. **Register on Steamworks**:
   - Go to [partner.steamgames.com](https://partner.steamgames.com) and create an app for your Steam AppID (`4206900`).
2. **Build and Upload with SteamPipe**:
   - Download the Steamworks SDK and locate `tools/ContentBuilder/`.
   - Set up your app depot to point to this game folder.
   - Run SteamPipe:
     ```
     steamcmd.exe +login <your_steam_account> +run_app_build ..\scripts\app_build_4206900.vdf +quit
     ```
3. **Configure Store Page**:
   - Copy descriptions and tags from `steam_store_metadata.json`.
   - Upload 1080p screenshots from gameplay.
4. **Publish**:
   - Set build to default branch and submit your store page for Steam review!
