# EvoWorld Asset Pipeline

## Verzió

v0.1.3

## Mappák

```text
assets/
├── ui/
├── sprites/
├── tiles/
├── backgrounds/
├── effects/
├── fonts/
├── sounds/
└── music/
```

## Kulcsok

Példa:

```text
assets/ui/button_blue.png
```

kulcsa:

```text
ui/button_blue
```

Használat:

```python
image = self.app.assets.get_image("ui/button_blue")
```
