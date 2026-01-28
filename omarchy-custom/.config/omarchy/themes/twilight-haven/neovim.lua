-- Twilight Haven colorscheme for Neovim
local colors = {
  background = "#0f0f14",
  foreground = "#e8e6e3",
  black = "#0f0f14",
  red = "#d4878f",
  green = "#a3b899",
  yellow = "#d4c087",
  blue = "#8fa3c4",
  magenta = "#b4a7d6",
  cyan = "#8fc4bc",
  white = "#c4c1bd",
  bright_black = "#3d3d47",
  bright_red = "#e0a0a8",
  bright_green = "#b8ccab",
  bright_yellow = "#e0d4a0",
  bright_blue = "#a8bcd8",
  bright_magenta = "#c9bce6",
  bright_cyan = "#a8d8ce",
  bright_white = "#e8e6e3",
}

-- Try to load catppuccin with custom colors
local ok, catppuccin = pcall(require, "catppuccin")
if ok then
  catppuccin.setup({
    flavour = "mocha",
    color_overrides = {
      mocha = {
        base = colors.background,
        mantle = "#0a0a0f",
        crust = "#050508",
        text = colors.foreground,
        subtext1 = colors.white,
        subtext0 = colors.bright_black,
        overlay2 = "#6e6e7a",
        overlay1 = "#5a5a66",
        overlay0 = "#464652",
        surface2 = colors.bright_black,
        surface1 = "#2d2d37",
        surface0 = "#1e1e27",
        lavender = colors.magenta,
        blue = colors.blue,
        sapphire = colors.cyan,
        sky = colors.bright_cyan,
        teal = colors.cyan,
        green = colors.green,
        yellow = colors.yellow,
        peach = colors.bright_yellow,
        maroon = colors.red,
        red = colors.bright_red,
        mauve = colors.bright_magenta,
        pink = colors.bright_magenta,
        flamingo = colors.bright_red,
        rosewater = colors.bright_red,
      },
    },
  })
  vim.cmd.colorscheme("catppuccin")
end

return colors
