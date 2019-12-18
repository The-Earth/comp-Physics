package main

import (
	"fmt"
	"math"
	"math/rand"
	"runtime"
	"time"
)

var dt float64 = 0.01
var t_max float64 = 50.
var num_of_atom int = 256
var T_eq float64 = 0.2
var max_x float64 = 10.
var max_y float64 = 10.

type Mass struct {
	x       float64
	prev_x  float64
	y       float64
	prev_y  float64
	vx      float64
	vy      float64
	ax      float64
	prev_ax float64
	ay      float64
	prev_ay float64
	k       float64
}

func (self Mass) update_r(_max_x float64, _max_y float64) Mass {
	self.prev_x, self.prev_y = self.x, self.y
	self.x = self.x + self.vx*dt + 0.5*self.ax*math.Pow(dt, 2.)
	self.y = self.y + self.vy*dt + 0.5*self.ay*math.Pow(dt, 2.)

	// Hard boundary
	if self.x > _max_x-0.2 || self.x < 0.2 {
		self.vx = -self.vx
	}
	if self.y > _max_y-0.2 || self.y < 0.2 {
		self.vy = -self.vy
	}

	return self
}

func (self Mass) update_v() Mass {
	self.vx = self.vx + 0.5*(self.prev_ax+self.ax)*dt
	self.vy = self.vy + 0.5*(self.prev_ay+self.ay)*dt
	return self
}

func (self Mass) update_a(all_atoms []Mass, prev bool) Mass {
	var ax float64 = 0
	var ay float64 = 0
	if prev {
		self.prev_ax, self.prev_ay = self.ax, self.ay
		return self
	}
	for _, _atom := range all_atoms {
		if self.x == _atom.x && self.y == _atom.y {
			continue
		}
		dx := self.x - _atom.x
		dy := self.y - _atom.y
		dr := math.Sqrt(math.Pow(dx, 2.) + math.Pow(dy, 2.))
		if dr < 0.8 { // cut-off
			ax += self.k * (2*math.Pow(dr, -13.) - math.Pow(dr, -7.)) * dx / dr
			ay += self.k * (2*math.Pow(dr, -13.) - math.Pow(dr, -7.)) * dy / dr
		}
	}

	self.ax, self.ay = ax, ay
	return self
}

func get_system_temperature(all_atoms []Mass, dimension int, amount int) float64 {
	var _sum float64 = 0.
	for _, _atom := range all_atoms {
		_sum += 0.5 * (math.Pow(_atom.vx, 2.) + math.Pow(_atom.vy, 2.))
	}
	return 2 * _sum / float64(dimension) / float64(amount)
}

func temperature_adjust(all_atoms []Mass, _T_cur float64) []Mass {
	for _, _atom := range all_atoms {
		_atom.vx = _atom.vx * math.Pow((T_eq/_T_cur), 0.5)
		_atom.vy = _atom.vy * math.Pow((T_eq/_T_cur), 0.5)
	}
	return all_atoms
}

func update_a_unit(_atom Mass, _atom_list []Mass, ret chan Mass) {
	_atom = _atom.update_a(_atom_list, true)
	_atom = _atom.update_a(_atom_list, false)
	ret <- _atom
}

func update_v_unit(_atom Mass, ret chan Mass) {
	_atom = _atom.update_v()
	ret <- _atom
}

func update_r_unit(_atom Mass, ret chan Mass) {
	_atom = _atom.update_r(max_x, max_y)
	ret <- _atom
}

func move_parallel(_atom_list []Mass) []Mass {
	res_a := make(chan Mass)
	var temp_a []Mass
	for _, _atom := range _atom_list {
		go update_a_unit(_atom, _atom_list, res_a)
	}
	for i := 0; i < len(_atom_list); i++ {
		temp_a = append(temp_a, <-res_a)
	}

	res_v := make(chan Mass)
	var temp_v []Mass
	for _, _atom := range temp_a {
		go update_v_unit(_atom, res_v)
	}
	for i := 0; i < len(_atom_list); i++ {
		temp_v = append(temp_v, <-res_v)
	}

	res_r := make(chan Mass)
	var temp_r []Mass
	for _, _atom := range temp_v {
		go update_r_unit(_atom, res_r)
	}
	for i := 0; i < len(_atom_list); i++ {
		temp_r = append(temp_r, <-res_r)
	}

	return temp_r
}

func move(_atom_list []Mass) []Mass {
	for i, _atom := range _atom_list {
		_atom = _atom.update_a(_atom_list, true)
		_atom = _atom.update_a(_atom_list, false)
		_atom_list[i] = _atom
	}
	for i, _atom := range _atom_list {
		_atom = _atom.update_v()
		_atom_list[i] = _atom
	}
	for i, _atom := range _atom_list {
		_atom = _atom.update_r(max_x, max_y)
		_atom_list[i] = _atom
	}

	return _atom_list
}

func maxwell_dist() float64 {
	for {
		_x := rand.Float64()*6 - 3
		_y := rand.Float64()
		if _y < math.Pow(_x, 2)*math.Exp(math.Pow(-_x, 2)) {
			return _x
		}
	}
}

func initialization() []Mass {
	var _atom_list []Mass
	for i := 0; i < num_of_atom; i++ {
		var x0 float64 = 0.55*float64(i%16) + (rand.Float64()/5. + 0.9)
		var y0 float64 = 0.55*float64(i/16) + (rand.Float64()/5. + 0.9)
		var v0 float64 = 0.1 * maxwell_dist()
		theta0 := rand.Float64() * 2. * math.Pi
		_atom := Mass{x0, x0, y0, y0, v0 * math.Cos(theta0), v0 * math.Sin(theta0),
			0., 0., 0., 0., 1e-7}
		_atom_list = append(_atom_list, _atom)
	}
	return _atom_list
}

func main() {
	rand.Seed(time.Now().Unix())
	runtime.GOMAXPROCS(2)

	var T_list []float64
	var t_list []float64
	atom_list := initialization()
	var cur_t float64 = 0.

	for cur_t < t_max {
		atom_list = move_parallel(atom_list)
		T_cur := get_system_temperature(atom_list, 2, num_of_atom)
		T_list = append(T_list, T_cur)
		t_list = append(t_list, cur_t)
		fmt.Println(cur_t / t_max)
		fmt.Println(T_cur)
		cur_t += dt
	}
}
