# ---------------------------------------------------------------

# SSH is laggy over the wifi, disabling wifi power saving helps

# NM_SETTING_WIRELESS_POWERSAVE_DEFAULT (0): use the default value
# NM_SETTING_WIRELESS_POWERSAVE_IGNORE  (1): don't touch existing setting
# NM_SETTING_WIRELESS_POWERSAVE_DISABLE (2): disable powersave
# NM_SETTING_WIRELESS_POWERSAVE_ENABLE  (3): enable powersave
echo -e "[connection]\nwifi.powersave = 2" > /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf

# ---------------------------------------------------------------

# Install docker (see https://docs.docker.com/engine/install/ubuntu/)
apt-get update

apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update

apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# ---------------------------------------------------------------

# Post docker install setup

groupadd docker

usermod -aG docker vbauer
