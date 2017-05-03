
_kubos()
{
    output="$(python /home/vagrant/.complete.py ${COMP_LINE})"
    IFS=' ' read -r -a COMPREPLY <<< "$output"
}

complete -F _kubos kubos
