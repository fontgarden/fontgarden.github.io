document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('opticalSizeSlider');
    const sampleTexts = document.querySelectorAll('.sampleText');
    const sliderValue = document.getElementById('sliderValue');

    slider.addEventListener('input', function() {
        const opticalSize = slider.value;
        sampleTexts.forEach(sampleText => {
            sampleText.style.fontVariationSettings = `'opsz' ${opticalSize}`;
        });
        sliderValue.textContent = opticalSize;
    });
});

