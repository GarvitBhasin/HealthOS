export function getCredentials(element1, element2) {
    const value1 = document.querySelector(element1).value;
    const value2 = document.querySelector(element2).value;

    return [value1, value2];
}